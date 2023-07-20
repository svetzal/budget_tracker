import datetime
from _decimal import Decimal

import pandas as pd

from entities import CoachingPracticeFinance, TransactionAgreement, Contractor, Consultancy, Invoice, HoursLineItem, \
    ExpenseLineItem, FundingSource, SupportArea, AreaAssignment, Employee, Person
from data_types import Money


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
        candidates = [c for c in self.practice.contractors if c.code == contractor_code]
        if len(candidates) == 0:
            raise ValueError(f"Contractor {contractor_code} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Contractor {contractor_code} is ambiguous (found multiple)")
        return candidates[0]

    def aggregate_contractors_employees(self):
        people: list[Person] = []
        for p in self.practice.contractors:
            people.append(p)
        for p in self.practice.employees:
            people.append(p)
        return people

    def count_business_days_between_dates(self, start_date: datetime.date, end_date: datetime.date) -> int:
        return pd.bdate_range(start_date, end_date, freq='C', holidays=self.practice.statutory_holiday_list).size



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
    def execute(self, code: str, name: str, consultancy_code: str, email: str, start_date: str,
                phone_number: str = None, end_date: str = None):
        contractor = Contractor(
            code=code,
            name=name,
            email=email,
            start_date=start_date,
            consultancy_code=consultancy_code,
            phone_number=phone_number,
            end_date=datetime.date.fromisoformat(end_date) if end_date else None,
        )
        if contractor.consultancy_code not in [c.code for c in self.practice.consultancies]:
            raise ValueError(f"Consultancy {contractor.consultancy_code} does not exist")
        if contractor not in self.practice.contractors:
            self.practice.contractors.append(contractor)


class AddEmployee(UseCase):
    def execute(self, code: str, name: str, email: str, start_date: str, end_date: str = None, phone_number: str = None):
        employee = Employee(
            code=code,
            name=name,
            email=email,
            start_date=start_date,
            phone_number=phone_number,
            end_date=datetime.date.fromisoformat(end_date) if end_date else None,
        )
        if employee not in self.practice.employees:
            self.practice.employees.append(employee)


class AddTransactionAgreement(UseCase):
    def execute(self, number: str, contractor_code: str, hours: int, rate: float, start_date: datetime.date, end_date: datetime.date):
        transaction_agreement = TransactionAgreement(
            number=number,
            contractor_code=contractor_code,
            hours=hours,
            rate=Money(root=Decimal(rate)),
            start_date=start_date,
            end_date=end_date
        )
        if transaction_agreement not in self.practice.transaction_agreements:
            self.practice.transaction_agreements.append(transaction_agreement)


class AddInvoice(UseCase):
    def execute(self, **kwargs):
        invoice = Invoice(**kwargs)
        consultancy = self.find_consultancy_by_code(kwargs['consultancy_code'])
        if invoice not in consultancy.invoices:
            consultancy.invoices.append(invoice)


class AddHoursLineItemToInvoice(UseCase):
    def execute(self, invoice_number: str, description: str, amount: Decimal, contractor_code: str, taxable: bool, hours: int):
        line_item = HoursLineItem(
            description=description,
            amount=Money(root=amount),
            contractor_code=contractor_code,
            taxable=taxable,
            hours=hours
        )
        invoice = self.find_invoice(invoice_number)
        if line_item not in invoice.line_items:
            invoice.line_items.append(line_item)


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


class MarkInvoiceAsPaid(UseCase):
    def execute(self, invoice_number):
        invoice = self.find_invoice(invoice_number)
        invoice.paid = True


class AddFundingSource(UseCase):
    def execute(self, transit: int, name: str, total: Decimal, start_date: str, end_date: str):
        funding_source = FundingSource(
            transit=transit,
            name=name,
            total=Money(root=total),
            start_date=datetime.date.fromisoformat(start_date),
            end_date=datetime.date.fromisoformat(end_date)
        )
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
