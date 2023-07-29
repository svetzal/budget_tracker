from entities import Consultancy
from use_cases.use_case import UseCase


class AddConsultancy(UseCase):
    def execute(self, code: str, name: str, contract: str, contact_name: str, contact_phone: str, contact_email: str):
        self.guard_consultancy_duplicate(code)
        consultancy = Consultancy(
            code=code,
            name=name,
            contract=contract,
            contact_name=contact_name,
            contact_phone=contact_phone,
            contact_email=contact_email
        )
        self.practice.consultancies.append(consultancy)
