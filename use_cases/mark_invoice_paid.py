from use_cases.use_case import UseCase


class MarkInvoiceAsPaid(UseCase):
    def execute(self, invoice_number):
        invoice = self.find_invoice(invoice_number)
        invoice.paid = True
