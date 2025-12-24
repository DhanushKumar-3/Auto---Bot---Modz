from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from stock.models import Stock, StockLog

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

def login_required():
    return "admin_id" in session

@stock_bp.route("/")
def list_stock():
    if not login_required():
        return redirect(url_for("auth.login"))

    stocks = Stock.query.filter_by(is_active=True).all()
    return render_template("stock/list.html", stocks=stocks)

@stock_bp.route("/add", methods=["GET", "POST"])
@stock_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def add_edit_stock(id=None):
    if not login_required():
        return redirect(url_for("auth.login"))

    stock = Stock.query.get(id) if id else None

    if request.method == "POST":
        qty = int(request.form["quantity"])
        if qty < 0:
            flash("Quantity cannot be negative", "danger")
            return redirect(request.url)

        if not stock:
            stock = Stock(part_number=request.form["part_number"])

        stock.part_name = request.form["part_name"]
        stock.brand = request.form["brand"]
        stock.bike_model = request.form["bike_model"]
        stock.purchase_price = float(request.form["purchase_price"])
        stock.selling_price = float(request.form["selling_price"])
        stock.quantity = qty
        stock.min_quantity = int(request.form["min_quantity"])

        db.session.add(stock)
        db.session.commit()

        db.session.add(StockLog(
            stock_id=stock.id,
            change_qty=qty,
            reason="Manual update"
        ))
        db.session.commit()

        flash("Stock saved successfully", "success")
        return redirect(url_for("stock.list_stock"))

    return render_template("stock/add_edit.html", stock=stock)

@stock_bp.route("/delete/<int:id>")
def delete_stock(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    stock = Stock.query.get_or_404(id)
    stock.is_active = False
    db.session.commit()

    flash("Stock deleted", "warning")
    return redirect(url_for("stock.list_stock"))
