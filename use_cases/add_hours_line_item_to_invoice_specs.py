from entities import CoachingPracticeFinance
from use_cases.add_hours_line_item_to_invoice import AddHoursLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from verifiers import verify_model


def test_can_add_hours_invoice_for_consultancy(staffed_practice: CoachingPracticeFinance, first_invoice_details: dict,
                                               first_hours_line_item_details: dict):
    AddInvoice(staffed_practice).execute(**first_invoice_details)
    AddHoursLineItemToInvoice(staffed_practice).execute(**first_hours_line_item_details)

    verify_model(staffed_practice.consultancies)
