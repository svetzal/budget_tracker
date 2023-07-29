from _decimal import Decimal

from data_types import Money
from entities import HoursLineItem
from use_cases.use_case import UseCase


class AddHoursLineItemToInvoice(UseCase):
    def execute(self, invoice_number: str, description: str, amount: Decimal, contractor_code: str, taxable: bool, hours: int):
        line_item = HoursLineItem(
            description=description,
            amount=Money(root=amount),
            contractor_code=contractor_code,
            taxable=taxable,
            hours=hours
        )
        invoice = self.find_invoice(invoice_number)
        if line_item not in invoice.line_items:
            invoice.line_items.append(line_item)
