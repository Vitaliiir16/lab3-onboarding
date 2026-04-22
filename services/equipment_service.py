from sqlalchemy.orm import Session
from models.equipment import Equipment
from models.employee import Employee


class EquipmentService:
    """Business logic service for equipment management."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Equipment]:
        """Retrieve all equipment ordered by ID descending."""
        return (
            self.session.query(Equipment)
            .order_by(Equipment.id.desc())
            .all()
        )

    def get_by_id(self, equipment_id: int) -> Equipment | None:
        """Retrieve a single equipment item by ID."""
        return self.session.get(Equipment, equipment_id)

    def get_all_employees(self) -> list[Employee]:
        """Retrieve all employees for the form dropdown."""
        return self.session.query(Employee).order_by(Employee.name).all()

    def create(
        self,
        serial_number: str,
        equipment_type: str,
        model: str,
        employee_id: int,
    ) -> Equipment:
        """Add a new equipment item."""
        if not serial_number or not equipment_type or not model or not employee_id:
            raise ValueError("All fields are required")

        existing = (
            self.session.query(Equipment)
            .filter(Equipment.serial_number == serial_number.strip())
            .first()
        )
        if existing:
            raise ValueError(
                f"Equipment with serial number '{serial_number}' already exists"
            )

        # Verify the employee exists
        employee = self.session.get(Employee, int(employee_id))
        if employee is None:
            raise ValueError("Employee not found")

        equipment = Equipment(
            serial_number=serial_number.strip(),
            equipment_type=equipment_type.strip(),
            model=model.strip(),
            employee_id=int(employee_id),
        )
        self.session.add(equipment)
        self.session.commit()
        return equipment

    def update(
        self,
        equipment_id: int,
        serial_number: str,
        equipment_type: str,
        model: str,
        employee_id: int,
    ) -> Equipment:
        """Update an existing equipment item."""
        equipment = self.get_by_id(equipment_id)
        if equipment is None:
            raise ValueError("Equipment not found")

        if not serial_number or not equipment_type or not model or not employee_id:
            raise ValueError("All fields are required")

        # Check serial number uniqueness
        existing = (
            self.session.query(Equipment)
            .filter(
                Equipment.serial_number == serial_number.strip(),
                Equipment.id != equipment_id,
            )
            .first()
        )
        if existing:
            raise ValueError(
                f"Equipment with serial number '{serial_number}' already exists"
            )

        equipment.serial_number = serial_number.strip()
        equipment.equipment_type = equipment_type.strip()
        equipment.model = model.strip()
        equipment.employee_id = int(employee_id)
        self.session.commit()
        return equipment

    def delete(self, equipment_id: int) -> None:
        """Delete an equipment item."""
        equipment = self.get_by_id(equipment_id)
        if equipment is None:
            raise ValueError("Equipment not found")
        self.session.delete(equipment)
        self.session.commit()

    def count(self) -> int:
        """Return total number of equipment items."""
        return self.session.query(Equipment).count()
