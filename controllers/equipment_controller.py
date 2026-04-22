from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_session
from services.equipment_service import EquipmentService

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@equipment_bp.route("/")
def list_equipment():
    """Display the list of all equipment."""
    session = get_session()
    try:
        service = EquipmentService(session)
        equipment_list = service.get_all()
        return render_template("equipment/list.html", equipment_list=equipment_list)
    finally:
        session.close()


@equipment_bp.route("/create", methods=["GET", "POST"])
def create_equipment():
    """Show create form (GET) or add new equipment (POST)."""
    session = get_session()
    try:
        service = EquipmentService(session)

        if request.method == "POST":
            try:
                service.create(
                    serial_number=request.form.get("serial_number", ""),
                    equipment_type=request.form.get("equipment_type", ""),
                    model=request.form.get("model", ""),
                    employee_id=request.form.get("employee_id", 0),
                )
                flash("Equipment added successfully!", "success")
                return redirect(url_for("equipment.list_equipment"))
            except ValueError as e:
                flash(str(e), "error")
                employees = service.get_all_employees()
                return render_template(
                    "equipment/form.html",
                    equipment=None,
                    employees=employees,
                    error=str(e),
                )

        employees = service.get_all_employees()
        return render_template(
            "equipment/form.html", equipment=None, employees=employees
        )
    finally:
        session.close()


@equipment_bp.route("/<int:equipment_id>/edit", methods=["GET", "POST"])
def edit_equipment(equipment_id: int):
    """Show edit form (GET) or update equipment (POST)."""
    session = get_session()
    try:
        service = EquipmentService(session)

        if request.method == "POST":
            try:
                service.update(
                    equipment_id=equipment_id,
                    serial_number=request.form.get("serial_number", ""),
                    equipment_type=request.form.get("equipment_type", ""),
                    model=request.form.get("model", ""),
                    employee_id=request.form.get("employee_id", 0),
                )
                flash("Equipment updated successfully!", "success")
                return redirect(url_for("equipment.list_equipment"))
            except ValueError as e:
                flash(str(e), "error")
                equipment = service.get_by_id(equipment_id)
                employees = service.get_all_employees()
                return render_template(
                    "equipment/form.html",
                    equipment=equipment,
                    employees=employees,
                    error=str(e),
                )

        equipment = service.get_by_id(equipment_id)
        if equipment is None:
            flash("Equipment not found!", "error")
            return redirect(url_for("equipment.list_equipment"))
        employees = service.get_all_employees()
        return render_template(
            "equipment/form.html", equipment=equipment, employees=employees
        )
    finally:
        session.close()


@equipment_bp.route("/<int:equipment_id>/delete", methods=["POST"])
def delete_equipment(equipment_id: int):
    """Delete an equipment item by ID."""
    session = get_session()
    try:
        service = EquipmentService(session)
        try:
            service.delete(equipment_id)
            flash("Equipment deleted!", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("equipment.list_equipment"))
    finally:
        session.close()
