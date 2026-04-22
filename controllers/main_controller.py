from flask import Blueprint, render_template
from db import get_session
from services.employee_service import EmployeeService
from services.equipment_service import EquipmentService
from services.account_service import AccountService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Dashboard page with summary statistics."""
    session = get_session()
    try:
        emp_service = EmployeeService(session)
        equip_service = EquipmentService(session)
        acc_service = AccountService(session)

        stats = {
            "employees": emp_service.count(),
            "equipment": equip_service.count(),
            "accounts": acc_service.count(),
        }

        recent_employees = emp_service.get_all()[:5]

        return render_template(
            "index.html", stats=stats, recent_employees=recent_employees
        )
    finally:
        session.close()
