from flask import Blueprint, render_template, request, redirect, url_for, session, flash,make_response
from extensions import db
from billing.models import Bill, BillItem
from stock.models import Stock, StockLog
from customers.models import Customer
from datetime import datetime,date
from sqlalchemy import func
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from config import ShopConfig

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")

def login_required():
    return "admin_id" in session

def generate_bill_no():
    today = datetime.now().strftime("%Y%m%d")
    count = Bill.query.count() + 1
    return f"BILL-{today}-{count}"

@billing_bp.route("/create", methods=["GET", "POST"])
def create_bill():
    if not login_required():
        return redirect(url_for("auth.login"))

    stocks = Stock.query.filter_by(is_active=True).all()

    if request.method == "POST":
        mobile = request.form["mobile"]
        name = request.form["name"]
        address = request.form["address"]

        customer = Customer.query.filter_by(mobile=mobile).first()
        if not customer:
            customer = Customer(name=name, mobile=mobile, address=address)
            db.session.add(customer)
            db.session.commit()

        bill = Bill(
            bill_no=generate_bill_no(),
            customer_id=customer.id
        )
        db.session.add(bill)
        db.session.commit()

        total_amount = 0
        total_profit = 0

        for stock in stocks:
            raw_qty = request.form.get(f"qty_{stock.id}")
            qty = int(raw_qty) if raw_qty and raw_qty.isdigit() else 0

            if qty > 0:
                if qty > stock.quantity:
                    flash(f"Insufficient stock for {stock.part_name}", "danger")
                    return redirect(url_for("billing.create_bill"))

                profit = (stock.selling_price - stock.purchase_price) * qty
                total_profit += profit
                total_amount += stock.selling_price * qty

                stock.quantity -= qty

                db.session.add(BillItem(
                    bill_id=bill.id,
                    stock_id=stock.id,
                    quantity=qty,
                    selling_price=stock.selling_price,
                    profit=profit
                ))

                db.session.add(StockLog(
                    stock_id=stock.id,
                    change_qty=-qty,
                    reason="Sold"
                ))


        bill.total_amount = total_amount
        bill.total_profit = total_profit
        cgst = total_amount * ShopConfig.CGST_PERCENT / 100
        sgst = total_amount * ShopConfig.SGST_PERCENT / 100

        bill.total_amount = total_amount
        bill.total_profit = total_profit
        bill.cgst_amount = cgst
        bill.sgst_amount = sgst
        bill.grand_total = total_amount + cgst + sgst

        db.session.commit()

        flash("Bill created successfully", "success")
        return redirect(url_for("billing.view_bill", id=bill.id))

    return render_template("billing/create_bill.html", stocks=stocks)

@billing_bp.route("/view/<int:id>")
def view_bill(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    bill = Bill.query.get_or_404(id)
    customer = Customer.query.get(bill.customer_id)
    return render_template("billing/view_bill.html", bill=bill, customer=customer)

@billing_bp.route("/today")
def today_sales():
    if "admin_id" not in session:
        return redirect(url_for("auth.login"))

    today = date.today()
    bills = Bill.query.filter(func.date(Bill.created_at) == today).all()

    return render_template("sales_today.html", bills=bills)

@billing_bp.route("/invoice/pdf/<int:id>")
def invoice_pdf(id):
    if "admin_id" not in session:
        return redirect(url_for("auth.login"))

    bill = Bill.query.get_or_404(id)
    customer = Customer.query.get(bill.customer_id)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40

    # 🏪 SHOP HEADER
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, y, ShopConfig.SHOP_NAME)
    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(width / 2, y, f"GSTIN: {ShopConfig.GST_NUMBER}")
    y -= 30

    # 📄 INVOICE INFO
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, y, f"Invoice No: {bill.bill_no}")
    pdf.drawRightString(width - 40, y, f"Date: {bill.created_at.strftime('%d-%m-%Y %H:%M')}")
    y -= 15

    pdf.drawString(40, y, f"Customer: {customer.name} ({customer.mobile})")
    y -= 25

    # 🧾 TABLE HEADER
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, "Item")
    pdf.drawString(260, y, "Qty")
    pdf.drawString(310, y, "Rate")
    pdf.drawString(380, y, "Amount")
    y -= 8
    pdf.line(40, y, width - 40, y)
    y -= 15

    pdf.setFont("Helvetica", 10)

    # 🧾 ITEMS
    for item in bill.items:
        stock = Stock.query.get(item.stock_id)

        product_text = f"{stock.part_name} (PN: {stock.part_number})"

        pdf.drawString(40, y, product_text)
        pdf.drawString(260, y, str(item.quantity))
        pdf.drawString(310, y, f"₹{item.selling_price:.2f}")
        pdf.drawString(380, y, f"₹{item.quantity * item.selling_price:.2f}")
        y -= 18

        if y < 120:
            pdf.showPage()
            y = height - 50

    # 🧮 TOTALS
    y -= 10
    pdf.line(300, y, width - 40, y)
    y -= 20

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(width - 40, y, f"Sub Total: ₹{bill.total_amount:.2f}")
    y -= 15
    pdf.drawRightString(width - 40, y, f"CGST ({ShopConfig.CGST_PERCENT}%): ₹{bill.cgst_amount:.2f}")
    y -= 15
    pdf.drawRightString(width - 40, y, f"SGST ({ShopConfig.SGST_PERCENT}%): ₹{bill.sgst_amount:.2f}")
    y -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(width - 40, y, f"Grand Total: ₹{bill.grand_total:.2f}")
    y -= 30

    # © FOOTER
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(width / 2, y, f"© {ShopConfig.SHOP_NAME} – All Rights Reserved")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename={bill.bill_no}.pdf"

    return response
