import datetime

from entities import Contractor
from use_cases.use_case import UseCase


class AddContractor(UseCase):
    def execute(self, code: str, name: str, consultancy_code: str, email: str, start_date: str,
                phone_number: str = None, end_date: str = None):
        self.guard_consultancy_must_exist(consultancy_code)
        self.guard_contractor_not_duplicate(code)
        contractor = Contractor(
            code=code,
            name=name,
            email=email,
            start_date=start_date,
            consultancy_code=consultancy_code,
            phone_number=phone_number,
            end_date=datetime.date.fromisoformat(end_date) if end_date else None,
        )
        self.practice.contractors.append(contractor)
