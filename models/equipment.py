from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


class Equipment(Base):
    """Equipment model — hardware assigned to an employee during onboarding."""

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    equipment_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # laptop | monitor | keyboard | mouse | headset
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("employees.id"), nullable=False
    )

    # Relationship
    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="equipment_list"
    )

    def __repr__(self) -> str:
        return f"<Equipment {self.equipment_type} — {self.model}>"


from models.employee import Employee  # noqa: E402, F401
