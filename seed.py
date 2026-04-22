"""
Database seed script — populates the database with test data.
Run once: python seed.py
"""
from datetime import date
from db import init_db, get_session
from models.employee import Employee
from models.equipment import Equipment
from models.account import Account


def seed():
    init_db()
    session = get_session()

    # Skip if data already exists
    if session.query(Employee).count() > 0:
        print("Database already contains data. Seed skipped.")
        session.close()
        return

    # Employees
    employees_data = [
        Employee(
            name="Ivan Petrenko",
            email="ivan.petrenko@company.com",
            position="Software Engineer",
            start_date=date(2024, 3, 1),
            status="completed",
        ),
        Employee(
            name="Olena Kovalenko",
            email="olena.kovalenko@company.com",
            position="QA Engineer",
            start_date=date(2024, 3, 15),
            status="completed",
        ),
        Employee(
            name="Maksym Bondarenko",
            email="maksym.bondarenko@company.com",
            position="DevOps Engineer",
            start_date=date(2024, 4, 1),
            status="in_progress",
        ),
        Employee(
            name="Sofiia Melnyk",
            email="sofiia.melnyk@company.com",
            position="Frontend Developer",
            start_date=date(2024, 4, 10),
            status="in_progress",
        ),
        Employee(
            name="Taras Shevchenko",
            email="taras.shevchenko@company.com",
            position="Backend Developer",
            start_date=date(2024, 5, 1),
            status="pending",
        ),
        Employee(
            name="Marta Kravets",
            email="marta.kravets@company.com",
            position="Project Manager",
            start_date=date(2024, 5, 15),
            status="pending",
        ),
        Employee(
            name="Nazar Polishchuk",
            email="nazar.polishchuk@company.com",
            position="Data Analyst",
            start_date=date(2024, 6, 1),
            status="pending",
        ),
    ]

    for emp in employees_data:
        session.add(emp)
    session.flush()

    # Equipment
    equipment_data = [
        Equipment(serial_number="SN-LP-001", equipment_type="laptop", model="MacBook Pro 16 M3", employee_id=employees_data[0].id),
        Equipment(serial_number="SN-MN-001", equipment_type="monitor", model="Dell U2723QE 27\"", employee_id=employees_data[0].id),
        Equipment(serial_number="SN-KB-001", equipment_type="keyboard", model="Logitech MX Keys", employee_id=employees_data[0].id),
        Equipment(serial_number="SN-LP-002", equipment_type="laptop", model="ThinkPad X1 Carbon Gen 11", employee_id=employees_data[1].id),
        Equipment(serial_number="SN-HS-001", equipment_type="headset", model="Jabra Evolve2 75", employee_id=employees_data[1].id),
        Equipment(serial_number="SN-LP-003", equipment_type="laptop", model="MacBook Pro 14 M3", employee_id=employees_data[2].id),
        Equipment(serial_number="SN-MN-002", equipment_type="monitor", model="LG 27UK850-W", employee_id=employees_data[2].id),
        Equipment(serial_number="SN-LP-004", equipment_type="laptop", model="Dell XPS 15", employee_id=employees_data[3].id),
        Equipment(serial_number="SN-MS-001", equipment_type="mouse", model="Logitech MX Master 3S", employee_id=employees_data[3].id),
        Equipment(serial_number="SN-LP-005", equipment_type="laptop", model="MacBook Air 15 M3", employee_id=employees_data[4].id),
    ]

    for eq in equipment_data:
        session.add(eq)

    # Accounts
    accounts_data = [
        Account(username="ivan.petrenko", system_name="email", permissions="write", is_active=True, employee_id=employees_data[0].id),
        Account(username="ivan.petrenko", system_name="jira", permissions="write", is_active=True, employee_id=employees_data[0].id),
        Account(username="ivan.petrenko", system_name="gitlab", permissions="write", is_active=True, employee_id=employees_data[0].id),
        Account(username="ivan.petrenko", system_name="slack", permissions="write", is_active=True, employee_id=employees_data[0].id),
        Account(username="olena.kovalenko", system_name="email", permissions="write", is_active=True, employee_id=employees_data[1].id),
        Account(username="olena.kovalenko", system_name="jira", permissions="admin", is_active=True, employee_id=employees_data[1].id),
        Account(username="maksym.bondarenko", system_name="email", permissions="write", is_active=True, employee_id=employees_data[2].id),
        Account(username="maksym.bondarenko", system_name="gitlab", permissions="admin", is_active=True, employee_id=employees_data[2].id),
        Account(username="maksym.bondarenko", system_name="vpn", permissions="admin", is_active=True, employee_id=employees_data[2].id),
        Account(username="sofiia.melnyk", system_name="email", permissions="read", is_active=False, employee_id=employees_data[3].id),
        Account(username="sofiia.melnyk", system_name="slack", permissions="write", is_active=False, employee_id=employees_data[3].id),
        Account(username="taras.shevchenko", system_name="email", permissions="read", is_active=False, employee_id=employees_data[4].id),
    ]

    for acc in accounts_data:
        session.add(acc)

    session.commit()
    session.close()

    print("Seed completed!")
    print(f"  Employees: {len(employees_data)}")
    print(f"  Equipment: {len(equipment_data)}")
    print(f"  Accounts: {len(accounts_data)}")


if __name__ == "__main__":
    seed()
