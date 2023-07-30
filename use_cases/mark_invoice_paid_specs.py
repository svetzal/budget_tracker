from entities import CoachingPracticeFinance
from use_cases.add_expense_line_item_to_invoice import AddExpenseLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from use_cases.mark_invoice_paid import MarkInvoiceAsPaid
from use_cases.test_data_generators import FIRST_INVOICE_NUMBER, FIRST_CONSULTANCY_CODE
from verifiers import verify_model


def test_can_mark_invoice_paid(staffed_practice: CoachingPracticeFinance, first_invoice_details: dict,
                               first_expense_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddExpenseLineItemToInvoice(staffed_practice).execute(**first_expense_details)

    MarkInvoiceAsPaid(staffed_practice).execute(FIRST_CONSULTANCY_CODE, FIRST_INVOICE_NUMBER, "2023-02-06")

    verify_model(staffed_practice.consultancies)
