from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


class Account(Base):
    """Account model — system account provisioned for an employee."""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    system_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # email | jira | gitlab | slack | vpn
    permissions: Mapped[str] = mapped_column(
        String(255), nullable=False, default="read"
    )  # read | write | admin
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("employees.id"), nullable=False
    )

    # Relationship
    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="accounts"
    )

    def __repr__(self) -> str:
        return f"<Account {self.username}@{self.system_name}>"


from models.employee import Employee  # noqa: E402, F401
