from flask import Flask, redirect, url_for, session
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # BLUEPRINT IMPORTS (AFTER db.init_app)
    from auth.routes import auth_bp
    from dashboard.routes import dashboard_bp
    from stock.routes import stock_bp
    from customers.routes import customers_bp
    from billing.routes import billing_bp
    from returns.routes import returns_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(returns_bp)

    with app.app_context():
        from auth.models import Admin
        db.create_all()

        if not Admin.query.first():
            admin = Admin.create_default_admin()
            db.session.add(admin)
            db.session.commit()

    @app.route("/")
    def root():
        if "admin_id" in session:
            return redirect(url_for("dashboard.home"))
        return redirect(url_for("auth.login"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
