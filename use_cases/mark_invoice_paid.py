from datetime import date

from use_cases.use_case import UseCase


class MarkInvoiceAsPaid(UseCase):
    def execute(self, consultancy: str, invoice_number: str, paid_date: str):
        for c in self.practice.consultancies:
            for i in c.invoices:
                if c.code == consultancy and i.number == invoice_number:
                    i.paid_date = date.fromisoformat(paid_date)
