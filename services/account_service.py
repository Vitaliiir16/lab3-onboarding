from sqlalchemy.orm import Session
from models.account import Account
from models.employee import Employee


class AccountService:
    """Business logic service for account management."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Account]:
        """Retrieve all accounts ordered by ID descending."""
        return (
            self.session.query(Account)
            .order_by(Account.id.desc())
            .all()
        )

    def get_by_id(self, account_id: int) -> Account | None:
        """Retrieve a single account by ID."""
        return self.session.get(Account, account_id)

    def get_all_employees(self) -> list[Employee]:
        """Retrieve all employees for the form dropdown."""
        return self.session.query(Employee).order_by(Employee.name).all()

    def create(
        self,
        username: str,
        system_name: str,
        permissions: str,
        is_active: bool,
        employee_id: int,
    ) -> Account:
        """Create a new system account."""
        if not username or not system_name or not permissions or not employee_id:
            raise ValueError("All fields are required")

        # Verify the employee exists
        employee = self.session.get(Employee, int(employee_id))
        if employee is None:
            raise ValueError("Employee not found")

        account = Account(
            username=username.strip(),
            system_name=system_name.strip(),
            permissions=permissions.strip(),
            is_active=bool(is_active),
            employee_id=int(employee_id),
        )
        self.session.add(account)
        self.session.commit()
        return account

    def update(
        self,
        account_id: int,
        username: str,
        system_name: str,
        permissions: str,
        is_active: bool,
        employee_id: int,
    ) -> Account:
        """Update an existing account."""
        account = self.get_by_id(account_id)
        if account is None:
            raise ValueError("Account not found")

        if not username or not system_name or not permissions or not employee_id:
            raise ValueError("All fields are required")

        account.username = username.strip()
        account.system_name = system_name.strip()
        account.permissions = permissions.strip()
        account.is_active = bool(is_active)
        account.employee_id = int(employee_id)
        self.session.commit()
        return account

    def delete(self, account_id: int) -> None:
        """Delete an account."""
        account = self.get_by_id(account_id)
        if account is None:
            raise ValueError("Account not found")
        self.session.delete(account)
        self.session.commit()

    def count(self) -> int:
        """Return total number of accounts."""
        return self.session.query(Account).count()
