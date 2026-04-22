from datetime import date, datetime
from sqlalchemy.orm import Session
from models.employee import Employee


class EmployeeService:
    """Business logic service for employee management."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Employee]:
        """Retrieve all employees ordered by ID descending."""
        return self.session.query(Employee).order_by(Employee.id.desc()).all()

    def get_by_id(self, employee_id: int) -> Employee | None:
        """Retrieve a single employee by ID."""
        return self.session.get(Employee, employee_id)

    def create(
        self,
        name: str,
        email: str,
        position: str,
        start_date: str,
        status: str = "pending",
    ) -> Employee:
        """Create a new employee record."""
        if not name or not email or not position or not start_date:
            raise ValueError("All fields are required")

        existing = (
            self.session.query(Employee).filter(Employee.email == email).first()
        )
        if existing:
            raise ValueError(f"Employee with email '{email}' already exists")

        employee = Employee(
            name=name.strip(),
            email=email.strip().lower(),
            position=position.strip(),
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(start_date, str)
            else start_date,
            status=status,
        )
        self.session.add(employee)
        self.session.commit()
        return employee

    def update(
        self,
        employee_id: int,
        name: str,
        email: str,
        position: str,
        start_date: str,
        status: str,
    ) -> Employee:
        """Update an existing employee record."""
        employee = self.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Employee not found")

        if not name or not email or not position or not start_date:
            raise ValueError("All fields are required")

        # Check email uniqueness excluding current employee
        existing = (
            self.session.query(Employee)
            .filter(Employee.email == email.strip().lower(), Employee.id != employee_id)
            .first()
        )
        if existing:
            raise ValueError(f"Employee with email '{email}' already exists")

        employee.name = name.strip()
        employee.email = email.strip().lower()
        employee.position = position.strip()
        employee.start_date = (
            datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(start_date, str)
            else start_date
        )
        employee.status = status
        self.session.commit()
        return employee

    def delete(self, employee_id: int) -> None:
        """Delete an employee and cascade to equipment and accounts."""
        employee = self.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Employee not found")
        self.session.delete(employee)
        self.session.commit()

    def count(self) -> int:
        """Return total number of employees."""
        return self.session.query(Employee).count()
