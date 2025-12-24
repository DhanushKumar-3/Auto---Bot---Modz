from flask import Blueprint, render_template, session, redirect, url_for
from datetime import date
from extensions import db
from stock.models import Stock
from billing.models import Bill, BillItem
from customers.models import Customer
from returns.models import Return
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

def login_required():
    return "admin_id" in session

@dashboard_bp.route("/")
def home():
    if not login_required():
        return redirect(url_for("auth.login"))

    today = date.today()

    total_stock = db.session.query(func.sum(Stock.quantity)).scalar() or 0

    today_bills = Bill.query.filter(func.date(Bill.created_at) == today).all()
    today_sales_qty = sum(item.quantity for bill in today_bills for item in bill.items)

    today_profit = sum(bill.total_profit for bill in today_bills)

    new_customers_today = Customer.query.filter(
        func.date(Customer.created_at) == today
    ).count()

    returns_today = Return.query.filter(
        func.date(Return.created_at) == today
    ).all()

    total_returns_today = sum(r.quantity for r in returns_today)

    monthly_returns = Return.query.filter(
        func.strftime('%Y-%m', Return.created_at) == today.strftime('%Y-%m')
    ).count()

    # Chart data
    stock_by_brand = (
        db.session.query(Stock.brand, func.sum(Stock.quantity))
        .group_by(Stock.brand)
        .all()
    )
    low_stock_items = Stock.query.filter(Stock.quantity <= Stock.min_quantity,Stock.is_active == True).all()

    return render_template(
        "dashboard.html",
        total_stock=total_stock,
        today_sales_qty=today_sales_qty,
        today_profit=today_profit,
        new_customers_today=new_customers_today,
        total_returns_today=total_returns_today,
        monthly_returns=monthly_returns,
        stock_by_brand=stock_by_brand
    )
