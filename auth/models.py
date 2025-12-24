from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @staticmethod
    def create_default_admin():
        return Admin(
            username="admin",
            password_hash=generate_password_hash("admin123")
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
