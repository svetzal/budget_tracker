import datetime

import pandas as pd

from entities import CoachingPracticeFinance, Consultancy, Invoice, Person


class UseCase:
    practice: CoachingPracticeFinance

    def __init__(self, practice: CoachingPracticeFinance):
        self.practice = practice

    def guard_consultancy_exists(self, consultancy_code):
        if not consultancy_code in [c.code for c in self.practice.consultancies]:
            raise ValueError(f"Consultancy {consultancy_code} does not exist")

    def guard_contractor_exists(self, contractor_code):
        if not contractor_code in [c.code for c in self.practice.contractors]:
            raise ValueError(f"Contractor {contractor_code} does not exist")

    def guard_contractor_duplicate(self, code):
        if code in [c.code for c in self.practice.contractors]:
            raise ValueError(f"Contractor {code} already exists")

    def guard_employee_duplicate(self, code: str):
        if code in [e.code for e in self.practice.employees]:
            raise ValueError(f"Employee {code} already exists")

    def guard_transaction_agreement_duplicate(self, number):
        if number in [t.number for t in self.practice.transaction_agreements]:
            raise ValueError(f"Transaction agreement {number} already exists")

    def guard_support_area_exists(self, support_area_code):
        if not support_area_code in [a.code for a in self.practice.support_areas]:
            raise ValueError(f"Support area {support_area_code} does not exist")

    def guard_support_area_duplicate(self, support_area_code: str):
        if support_area_code in [a.code for a in self.practice.support_areas]:
            raise ValueError(f"Support area {support_area_code} already exists")

    def guard_funding_source_exists(self, funding_source_transit):
        if not funding_source_transit in [f.transit for f in self.practice.funding_sources]:
            raise ValueError(f"Funding source {funding_source_transit} does not exist")

    def guard_consultancy_duplicate(self, code: str):
        if code in [c.code for c in self.practice.consultancies]:
            raise ValueError(f"Consultancy {code} already exists")

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

    def find_employee(self, employee_code):
        candidates = [e for e in self.practice.employees if e.code == employee_code]
        if len(candidates) == 0:
            raise ValueError(f"Employee {employee_code} does not exist")
        if (len(candidates) > 1):
            raise ValueError(f"Employee {employee_code} is ambiguous (found multiple)")
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
