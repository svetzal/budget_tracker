from datetime import date

from use_cases.use_case import UseCase


class MarkInvoiceAsPaid(UseCase):
    def execute(self, invoice_number: str, paid_date: str):
        invoice = self.find_invoice(invoice_number)
        invoice.paid_date = date.fromisoformat(paid_date)
