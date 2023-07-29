from _decimal import Decimal

from entities import CoachingPracticeFinance
from use_cases.add_expense_line_item_to_invoice import AddExpenseLineItemToInvoice
from use_cases.add_hours_line_item_to_invoice import AddHoursLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from use_cases.mark_invoice_paid import MarkInvoiceAsPaid
from use_cases.test_data_generators import FIRST_INVOICE_NUMBER
from verifiers import verify_model


def test_can_add_empty_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance, first_invoice_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)

    verify_model(staffed_practice.consultancies)


def test_can_add_hours_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance, first_invoice_details: dict,
                                               first_hours_line_item_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddHoursLineItemToInvoice(staffed_practice).execute(**first_hours_line_item_details)

    verify_model(staffed_practice.consultancies)


def test_can_add_expense_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance,
                                                 first_invoice_details: dict, first_expense_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddExpenseLineItemToInvoice(staffed_practice).execute(**first_expense_details)

    verify_model(staffed_practice.consultancies)


def test_can_mark_invoice_paid(staffed_practice: CoachingPracticeFinance, first_invoice_details: dict,
                               first_expense_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddExpenseLineItemToInvoice(staffed_practice).execute(**first_expense_details)

    MarkInvoiceAsPaid(staffed_practice).execute(FIRST_INVOICE_NUMBER, "2023-02-06")

    verify_model(staffed_practice.consultancies)
