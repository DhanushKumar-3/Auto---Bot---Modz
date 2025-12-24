from datetime import datetime
from extensions import db

class Bill(db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(20), unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    total_amount = db.Column(db.Float, default=0)
    total_profit = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cgst_amount = db.Column(db.Float, default=0)
    sgst_amount = db.Column(db.Float, default=0)
    grand_total = db.Column(db.Float, default=0)

    items = db.relationship("BillItem", backref="bill", lazy=True)

class BillItem(db.Model):
    __tablename__ = "bill_items"

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"))
    quantity = db.Column(db.Integer)
    selling_price = db.Column(db.Float)
    profit = db.Column(db.Float)
