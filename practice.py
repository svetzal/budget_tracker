import code

from entities import CoachingPracticeFinance
from report_use_cases import ListAreas, ListUnpaidInvoices, ListPeople, ListConsultancies, CurrentFiscalYearMonthly
from use_cases import AddConsultancy, AddContractor, AddTransactionAgreement, AddExpenseLineItemToInvoice, \
    AddHoursLineItemToInvoice, AddInvoice, MarkInvoiceAsPaid, \
    AddFundingSource, AddSupportArea, AddAreaAssignment, AddEmployee


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
