from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


class Employee(Base):
    """Employee model — main entity of the onboarding domain."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[str] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"
    )  # pending | in_progress | completed

    # Relationships
    equipment_list: Mapped[list["Equipment"]] = relationship(
        "Equipment", back_populates="employee", cascade="all, delete-orphan"
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account", back_populates="employee", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Employee {self.name} ({self.email})>"


from models.equipment import Equipment  # noqa: E402, F401
from models.account import Account  # noqa: E402, F401
