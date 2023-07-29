from _decimal import Decimal

from entities import CoachingPracticeFinance
from use_cases.add_expense_line_item_to_invoice import AddExpenseLineItemToInvoice
from use_cases.add_hours_line_item_to_invoice import AddHoursLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from verifiers import verify_model


def test_can_add_empty_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance):
    AddInvoice(staffed_practice).execute(
        consultancy_code=staffed_practice.consultancies[0].code,
        number="123",
        issue_date="2023-01-01"
    )

    verify_model(staffed_practice.consultancies)


def test_can_add_hours_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance):
    invoice_number = "123"
    AddInvoice(staffed_practice).execute(
        consultancy_code=staffed_practice.consultancies[0].code,
        number=invoice_number,
        issue_date="2023-01-07",
        paid_date="2023-02-06",
    )

    AddHoursLineItemToInvoice(staffed_practice).execute(
        invoice_number=invoice_number,
        description="Hours for first week",
        amount=Decimal(4000),
        contractor_code=staffed_practice.contractors[0].code,
        taxable=True,
        hours=40,
        period_start="2023-01-01",
        period_end="2023-01-07",
    )

    verify_model(staffed_practice.consultancies)

def test_can_add_expense_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance):
    invoice_number = "123"
    AddInvoice(staffed_practice).execute(
        consultancy_code=staffed_practice.consultancies[0].code,
        number=invoice_number,
        issue_date="2023-01-07",
        paid_date="2023-02-06",
    )

    AddExpenseLineItemToInvoice(staffed_practice).execute(
        invoice_number=invoice_number,
        description="Expenses for first week",
        amount=Decimal(100),
        contractor_code=staffed_practice.contractors[0].code,
        taxable=False,
    )

    verify_model(staffed_practice.consultancies)