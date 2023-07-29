import code

from entities import CoachingPracticeFinance
from use_cases.report_current_fiscal_year_monthly import CurrentFiscalYearMonthly
from use_cases.list_consultancies import ListConsultancies
from use_cases.list_people import ListPeople
from use_cases.list_unpaid_invoices import ListUnpaidInvoices
from use_cases.list_areas import ListAreas
from use_cases.add_area_assignment import AddAreaAssignment
from use_cases.add_support_area import AddSupportArea
from use_cases.add_funding_source import AddFundingSource
from use_cases.mark_invoice_paid import MarkInvoiceAsPaid
from use_cases.add_expense_line_item_to_invoice import AddExpenseLineItemToInvoice
from use_cases.add_hours_line_item_to_invoice import AddHoursLineItemToInvoice
from use_cases.add_invoice import AddInvoice
from use_cases.add_transaction_agreement import AddTransactionAgreement
from use_cases.add_employee import AddEmployee
from use_cases.add_contractor import AddContractor
from use_cases.add_consultancy import AddConsultancy


def main():
    practice = CoachingPracticeFinance.load()

    add_consultancy = AddConsultancy(practice)
    add_contractor = AddContractor(practice)
    add_transaction_agreement = AddTransactionAgreement(practice)
    list_consultancies = ListConsultancies(practice)
    list_people = ListPeople(practice)
    add_invoice = AddInvoice(practice)
    add_hours_line_item_to_invoice = AddHoursLineItemToInvoice(practice)
    add_expense_line_item_to_invoice = AddExpenseLineItemToInvoice(practice)
    list_unpaid_invoices = ListUnpaidInvoices(practice)
    mark_invoice_as_paid = MarkInvoiceAsPaid(practice)
    add_funding_source = AddFundingSource(practice)
    add_support_area = AddSupportArea(practice)
    add_area_assignment = AddAreaAssignment(practice)
    list_areas = ListAreas(practice)
    current_fiscal_year_monthly = CurrentFiscalYearMonthly(practice)
    add_employee = AddEmployee(practice)

    show = lambda use_case: print("\n".join(use_case.execute()))

    print("Digital Agile Coaching Practice")
    print("-------------------------------")
    print("")
    print("Available locals:")
    for key in locals().keys():
        print(f" - {key}")
    print("")

    console = code.InteractiveConsole(locals())
    console.interact()


if __name__ == "__main__":
    main()
