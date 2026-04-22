"""
Lab 3 — MVC Web Application
Domain: SAP SuccessFactors (People Onboarding)

Run: python app.py
"""
from flask import Flask
from config import Config
from db import init_db, ScopedSession

# Initialize Flask application
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize database (create DB + tables)
init_db()


# Close session after each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    ScopedSession.remove()


# Register controllers (Blueprints)
from controllers.main_controller import main_bp
from controllers.employee_controller import employee_bp
from controllers.equipment_controller import equipment_bp
from controllers.account_controller import account_bp

app.register_blueprint(main_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(account_bp)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
