from datetime import datetime
from extensions import db

class Return(db.Model):
    __tablename__ = "returns"

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"))
    quantity = db.Column(db.Integer, nullable=False)
    refund_amount = db.Column(db.Float, nullable=False)
    profit_reversed = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
