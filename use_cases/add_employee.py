import datetime

from entities import Employee
from use_cases.use_case import UseCase


class AddEmployee(UseCase):
    def execute(self, code: str, name: str, email: str, start_date: str, end_date: str = None, phone_number: str = None):
        self.guard_employee_not_duplicate(code)
        employee = Employee(
            code=code,
            name=name,
            email=email,
            start_date=start_date,
            phone_number=phone_number,
            end_date=datetime.date.fromisoformat(end_date) if end_date else None,
        )
        self.practice.employees.append(employee)
