from typing import Optional

from entities import Consultancy
from use_cases.use_case import UseCase


class AddConsultancy(UseCase):
    def execute(self, code: str, name: str, contract: str, contact_name: str, contact_phone: Optional[str] = None,
                contact_email: Optional[str] = None):
        self.guard_consultancy_not_duplicate(code)
        consultancy = Consultancy(
            code=code,
            name=name,
            contract=contract,
            contact_name=contact_name,
            contact_phone=contact_phone,
            contact_email=contact_email
        )
        self.practice.consultancies.append(consultancy)
