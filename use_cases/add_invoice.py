from datetime import date
from typing import Optional

from entities import Invoice
from use_cases.use_case import UseCase


class AddInvoice(UseCase):
    def execute(self, consultancy_code: str, number: str, issue_date: str, paid_date: Optional[str] = None):
        self.guard_consultancy_must_exist(consultancy_code)
        invoice = Invoice(
            number=number,
            consultancy_code=consultancy_code,
            issue_date=issue_date,
            paid_date=date.fromisoformat(paid_date) if paid_date else None
        )
        consultancy = self.find_consultancy_by_code(consultancy_code)
        consultancy.invoices.append(invoice)
