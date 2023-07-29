from entities import Invoice
from use_cases.use_case import UseCase


class AddInvoice(UseCase):
    def execute(self, **kwargs):
        invoice = Invoice(**kwargs)
        consultancy = self.find_consultancy_by_code(kwargs['consultancy_code'])
        if invoice not in consultancy.invoices:
            consultancy.invoices.append(invoice)
