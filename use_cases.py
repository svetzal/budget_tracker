from entities import CoachingPracticeFinance, TransactionAgreement, Contractor, Consultancy, Invoice, HoursLineItem, \
    ExpenseLineItem, FundingSource, SupportArea, AreaAssignment, Employee


class UseCase:
    practice: CoachingPracticeFinance

    def __init__(self, practice: CoachingPracticeFinance):
        self.practice = practice

    def find_consultancy_by_code(self, consultancy_code) -> Consultancy:
        if consultancy_code is None:
            return None
        candidates = [c for c in self.practice.consultancies if c.code == consultancy_code]
        if len(candidates) == 0:
            raise ValueError(f"Consultancy {consultancy_code} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Consultancy {consultancy_code} is ambiguous (found multiple)")
        return candidates[0]

    def find_consultancy_by_invoice(self, invoice_number) -> Consultancy:
        candidates = [c for c in self.practice.consultancies if invoice_number in [i.number for i in c.invoices]]
        if len(candidates) == 0:
            raise ValueError(f"Invoice {invoice_number} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Invoice {invoice_number} is ambiguous (found in multiple consultancies)")
        return candidates[0]

    def find_invoice(self, invoice_number) -> Invoice:
        candidates = [i for i in self.find_consultancy_by_invoice(invoice_number).invoices if
                      i.number == invoice_number]
        if len(candidates) == 0:
            raise ValueError(f"Invoice {invoice_number} does not exist")
        return candidates[0]

    def find_funding_source(self, transit):
        candidates = [f for f in self.practice.funding_sources if f.transit == transit]
        if len(candidates) == 0:
            raise ValueError(f"Funding source {transit} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Funding source {transit} is ambiguous (found multiple)")
        return candidates[0]

    def find_support_area(self, area_code):
        candidates = [a for a in self.practice.support_areas if a.code == area_code]
        if len(candidates) == 0:
            raise ValueError(f"Support area {area_code} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Support area {area_code} is ambiguous (found multiple)")
        return candidates[0]

    def find_contractor(self, contractor_code):
        candidates = [c for c in self.practice.people if c.code == contractor_code]
        if len(candidates) == 0:
            raise ValueError(f"Contractor {contractor_code} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Contractor {contractor_code} is ambiguous (found multiple)")
        return candidates[0]


class AddConsultancy(UseCase):
    def execute(self, code: str, name: str, contract: str, contact_name: str, contact_phone: str, contact_email: str):
        consultancy = Consultancy(
            code=code,
            name=name,
            contract=contract,
            contact_name=contact_name,
            contact_phone=contact_phone,
            contact_email=contact_email
        )
        if consultancy not in self.practice.consultancies:
            self.practice.consultancies.append(consultancy)


class AddContractor(UseCase):
    def execute(self, code: str, name: str, phone_number: str, email: str, start_date: str, consultancy_code: str):
        contractor = Contractor(code, name, phone_number, email, start_date, consultancy_code)
        if contractor.consultancy_code not in [c.code for c in self.practice.consultancies]:
            raise ValueError(f"Consultancy {contractor.consultancy_code} does not exist")
        if contractor not in self.practice.people:
            self.practice.people.append(contractor)


class AddEmployee(UseCase):
    def execute(self, code: str, name: str, phone_number: str, email: str, start_date: str):
        employee = Employee(code, name, phone_number, email, start_date)
        if employee not in self.practice.people:
            self.practice.people.append(employee)


class AddTransactionAgreement(UseCase):
    def execute(self, **kwargs):
        transaction_agreement = TransactionAgreement(**kwargs)
        if transaction_agreement not in self.practice.transaction_agreements:
            self.practice.transaction_agreements.append(transaction_agreement)


class AddInvoice(UseCase):
    def execute(self, **kwargs):
        invoice = Invoice(**kwargs)
        consultancy = self.find_consultancy_by_code(kwargs['consultancy_code'])
        if invoice not in consultancy.invoices:
            consultancy.invoices.append(invoice)


class AddHoursLineItemToInvoice(UseCase):
    def execute(self, **kwargs):
        line_item = HoursLineItem(**kwargs)
        invoice = self.find_invoice(kwargs['invoice_number'])
        if line_item not in invoice.line_items:
            invoice.line_items.append(line_item)


class AddExpenseLineItemToInvoice(UseCase):
    def execute(self, **kwargs):
        line_item = ExpenseLineItem(**kwargs)
        invoice = self.find_invoice(kwargs['invoice_number'])
        if line_item not in invoice.line_items:
            invoice.line_items.append(line_item)


class MarkInvoiceAsPaid(UseCase):
    def execute(self, invoice_number):
        invoice = self.find_invoice(invoice_number)
        invoice.paid = True


class AddFundingSource(UseCase):
    def execute(self, **kwargs):
        funding_source = FundingSource(**kwargs)
        if funding_source not in self.practice.funding_sources:
            self.practice.funding_sources.append(funding_source)


class AddSupportArea(UseCase):
    def execute(self, **kwargs):
        support_area = SupportArea(**kwargs)
        if support_area not in self.practice.support_areas:
            self.practice.support_areas.append(support_area)


class AddAreaAssignment(UseCase):
    def execute(self, **kwargs):
        self.find_support_area(kwargs['support_area_code'])
        self.find_contractor(kwargs['contractor_code'])
        self.find_funding_source(kwargs['funding_source_transit'])
        area_assignment = AreaAssignment(**kwargs)
        if area_assignment not in self.practice.area_assignments:
            self.practice.area_assignments.append(area_assignment)
