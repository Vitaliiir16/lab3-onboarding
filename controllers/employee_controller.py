from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_session
from services.employee_service import EmployeeService

employee_bp = Blueprint("employees", __name__, url_prefix="/employees")


@employee_bp.route("/")
def list_employees():
    """Display the list of all employees."""
    session = get_session()
    try:
        service = EmployeeService(session)
        employees = service.get_all()
        return render_template("employees/list.html", employees=employees)
    finally:
        session.close()


@employee_bp.route("/create", methods=["GET", "POST"])
def create_employee():
    """Show create form (GET) or process new employee (POST)."""
    if request.method == "POST":
        session = get_session()
        try:
            service = EmployeeService(session)
            service.create(
                name=request.form.get("name", ""),
                email=request.form.get("email", ""),
                position=request.form.get("position", ""),
                start_date=request.form.get("start_date", ""),
                status=request.form.get("status", "pending"),
            )
            flash("Employee created successfully!", "success")
            return redirect(url_for("employees.list_employees"))
        except ValueError as e:
            flash(str(e), "error")
            return render_template("employees/form.html", employee=None, error=str(e))
        finally:
            session.close()

    return render_template("employees/form.html", employee=None)


@employee_bp.route("/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee(employee_id: int):
    """Show edit form (GET) or update employee (POST)."""
    session = get_session()
    try:
        service = EmployeeService(session)

        if request.method == "POST":
            try:
                service.update(
                    employee_id=employee_id,
                    name=request.form.get("name", ""),
                    email=request.form.get("email", ""),
                    position=request.form.get("position", ""),
                    start_date=request.form.get("start_date", ""),
                    status=request.form.get("status", "pending"),
                )
                flash("Employee updated successfully!", "success")
                return redirect(url_for("employees.list_employees"))
            except ValueError as e:
                flash(str(e), "error")
                employee = service.get_by_id(employee_id)
                return render_template(
                    "employees/form.html", employee=employee, error=str(e)
                )

        employee = service.get_by_id(employee_id)
        if employee is None:
            flash("Employee not found!", "error")
            return redirect(url_for("employees.list_employees"))
        return render_template("employees/form.html", employee=employee)
    finally:
        session.close()


@employee_bp.route("/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id: int):
    """Delete an employee by ID."""
    session = get_session()
    try:
        service = EmployeeService(session)
        try:
            service.delete(employee_id)
            flash("Employee deleted!", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("employees.list_employees"))
    finally:
        session.close()
