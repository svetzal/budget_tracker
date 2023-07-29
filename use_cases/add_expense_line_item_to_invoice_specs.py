from entities import CoachingPracticeFinance
from use_cases.add_expense_line_item_to_invoice import AddExpenseLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from verifiers import verify_model


def test_can_add_expense_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance,
                                                 first_invoice_details: dict, first_expense_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddExpenseLineItemToInvoice(staffed_practice).execute(**first_expense_details)

    verify_model(staffed_practice.consultancies)
