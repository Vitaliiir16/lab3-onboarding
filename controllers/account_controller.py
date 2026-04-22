from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_session
from services.account_service import AccountService

account_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


@account_bp.route("/")
def list_accounts():
    """Display the list of all accounts."""
    session = get_session()
    try:
        service = AccountService(session)
        accounts = service.get_all()
        return render_template("accounts/list.html", accounts=accounts)
    finally:
        session.close()


@account_bp.route("/create", methods=["GET", "POST"])
def create_account():
    """Show create form (GET) or add new account (POST)."""
    session = get_session()
    try:
        service = AccountService(session)

        if request.method == "POST":
            try:
                service.create(
                    username=request.form.get("username", ""),
                    system_name=request.form.get("system_name", ""),
                    permissions=request.form.get("permissions", "read"),
                    is_active="is_active" in request.form,
                    employee_id=request.form.get("employee_id", 0),
                )
                flash("Account created successfully!", "success")
                return redirect(url_for("accounts.list_accounts"))
            except ValueError as e:
                flash(str(e), "error")
                employees = service.get_all_employees()
                return render_template(
                    "accounts/form.html",
                    account=None,
                    employees=employees,
                    error=str(e),
                )

        employees = service.get_all_employees()
        return render_template(
            "accounts/form.html", account=None, employees=employees
        )
    finally:
        session.close()


@account_bp.route("/<int:account_id>/edit", methods=["GET", "POST"])
def edit_account(account_id: int):
    """Show edit form (GET) or update account (POST)."""
    session = get_session()
    try:
        service = AccountService(session)

        if request.method == "POST":
            try:
                service.update(
                    account_id=account_id,
                    username=request.form.get("username", ""),
                    system_name=request.form.get("system_name", ""),
                    permissions=request.form.get("permissions", "read"),
                    is_active="is_active" in request.form,
                    employee_id=request.form.get("employee_id", 0),
                )
                flash("Account updated successfully!", "success")
                return redirect(url_for("accounts.list_accounts"))
            except ValueError as e:
                flash(str(e), "error")
                account = service.get_by_id(account_id)
                employees = service.get_all_employees()
                return render_template(
                    "accounts/form.html",
                    account=account,
                    employees=employees,
                    error=str(e),
                )

        account = service.get_by_id(account_id)
        if account is None:
            flash("Account not found!", "error")
            return redirect(url_for("accounts.list_accounts"))
        employees = service.get_all_employees()
        return render_template(
            "accounts/form.html", account=account, employees=employees
        )
    finally:
        session.close()


@account_bp.route("/<int:account_id>/delete", methods=["POST"])
def delete_account(account_id: int):
    """Delete an account by ID."""
    session = get_session()
    try:
        service = AccountService(session)
        try:
            service.delete(account_id)
            flash("Account deleted!", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("accounts.list_accounts"))
    finally:
        session.close()
