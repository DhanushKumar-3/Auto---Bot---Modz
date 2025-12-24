from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from customers.models import Customer

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def login_required():
    return "admin_id" in session

@customers_bp.route("/")
def list_customers():
    if not login_required():
        return redirect(url_for("auth.login"))

    q = request.args.get("q")
    if q:
        customers = Customer.query.filter(
            (Customer.mobile.contains(q)) | (Customer.name.contains(q))
        ).all()
    else:
        customers = Customer.query.all()

    return render_template("customers/list.html", customers=customers)

@customers_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    customer = Customer.query.get_or_404(id)

    if request.method == "POST":
        customer.name = request.form["name"]
        customer.mobile = request.form["mobile"]
        customer.address = request.form["address"]
        db.session.commit()

        flash("Customer updated", "success")
        return redirect(url_for("customers.list_customers"))

    return render_template("customers/edit.html", customer=customer)
