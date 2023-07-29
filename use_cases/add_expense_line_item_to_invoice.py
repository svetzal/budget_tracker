from _decimal import Decimal

from data_types import Money
from entities import ExpenseLineItem
from use_cases.use_case import UseCase


class AddExpenseLineItemToInvoice(UseCase):
    def execute(self, invoice_number: str, description: str, amount: Decimal, contractor_code: str, taxable: bool):
        line_item = ExpenseLineItem(
            description=description,
            amount=Money(root=amount),
            contractor_code=contractor_code,
            taxable=taxable
        )
        invoice = self.find_invoice(invoice_number)
        if line_item not in invoice.line_items:
            invoice.line_items.append(line_item)
