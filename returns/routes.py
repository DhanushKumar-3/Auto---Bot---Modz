from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from customers.models import Customer
from billing.models import Bill, BillItem
from stock.models import Stock, StockLog
from returns.models import Return

returns_bp = Blueprint("returns", __name__, url_prefix="/returns")

def login_required():
    return "admin_id" in session

# STEP 1: ENTER CUSTOMER MOBILE
@returns_bp.route("/", methods=["GET", "POST"])
def select_customer():
    if not login_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        mobile = request.form["mobile"]
        customer = Customer.query.filter_by(mobile=mobile).first()
        if not customer:
            flash("Customer not found", "danger")
            return redirect(request.url)

        return redirect(url_for("returns.select_bill", customer_id=customer.id))

    return render_template("returns/select_customer.html")

# STEP 2: SELECT BILL
@returns_bp.route("/bills/<int:customer_id>")
def select_bill(customer_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    bills = Bill.query.filter_by(customer_id=customer_id).all()
    return render_template("returns/select_bill.html", bills=bills)

# STEP 3: RETURN ITEMS
@returns_bp.route("/items/<int:bill_id>", methods=["GET", "POST"])
def return_items(bill_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    bill = Bill.query.get_or_404(bill_id)
    items = (db.session.query(BillItem, Stock).join(Stock, BillItem.stock_id == Stock.id).filter(BillItem.bill_id == bill_id).all()
)


    if request.method == "POST":
        for bill_item, stock in items:
            return_qty = int(request.form.get(f"return_{bill_item.id}", 0))

            if return_qty > 0:
                if return_qty >  bill_item.quantity:
                    flash("Return quantity exceeds sold quantity", "danger")
                    return redirect(request.url)

                refund = bill_item.selling_price * return_qty
                profit_reverse = (bill_item.selling_price - stock.purchase_price) * return_qty
                stock.quantity += return_qty
                bill.total_amount -= refund
                bill.total_profit -= profit_reverse
                bill.grand_total -= refund
                bill_item.quantity -= return_qty


                db.session.add(Return(
                    bill_id=bill.id,
                    stock_id=stock.id,
                    quantity=return_qty,
                    refund_amount=refund,
                    profit_reversed=profit_reverse
                ))

                db.session.add(StockLog(
                    stock_id=stock.id,
                    change_qty=return_qty,
                    reason="Returned"
                ))

        db.session.commit()
        flash("Return processed successfully", "success")
        return redirect(url_for("dashboard.home"))

    return render_template("returns/return_items.html", bill=bill, items=items)
