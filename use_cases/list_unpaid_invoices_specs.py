from entities import CoachingPracticeFinance
from use_cases.add_expense_line_item_to_invoice import AddExpenseLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from use_cases.list_unpaid_invoices import ListUnpaidInvoices
from verifiers import verify_report


def test_list_unpaid_invoices(staffed_practice: CoachingPracticeFinance,
                              first_invoice_details: dict, first_expense_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddExpenseLineItemToInvoice(staffed_practice).execute(**first_expense_details)

    output = ListUnpaidInvoices(staffed_practice).execute()

    verify_report(output)