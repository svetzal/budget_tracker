from datetime import date
from typing import List

import pandas as pd

from entities import CoachingPracticeFinance, Consultancy, Invoice, Person


class UseCase:
    practice: CoachingPracticeFinance

    def __init__(self, practice: CoachingPracticeFinance):
        self.practice = practice

    def guard_consultancy_must_exist(self, consultancy_code):
        if consultancy_code not in [c.code for c in self.practice.consultancies]:
            raise ValueError(f"Consultancy {consultancy_code} does not exist")

    def guard_contractor_must_exist(self, contractor_code):
        if contractor_code not in [c.code for c in self.practice.contractors]:
            raise ValueError(f"Contractor {contractor_code} does not exist")

    def guard_person_must_exist(self, person_code):
        if person_code not in [c.code for c in self.practice.contractors] and \
                person_code not in [e.code for e in self.practice.employees]:
            raise ValueError(f"Person {person_code} does not exist")

    def guard_contractor_not_duplicate(self, code):
        if code in [c.code for c in self.practice.contractors]:
            raise ValueError(f"Contractor {code} already exists")

    def guard_employee_not_duplicate(self, code: str):
        if code in [e.code for e in self.practice.employees]:
            raise ValueError(f"Employee {code} already exists")

    def guard_transaction_agreement_not_duplicate(self, number):
        if number in [t.number for t in self.practice.transaction_agreements]:
            raise ValueError(f"Transaction agreement {number} already exists")

    def guard_support_area_must_exist(self, support_area_code):
        if support_area_code not in [a.code for a in self.practice.support_areas]:
            raise ValueError(f"Support area {support_area_code} does not exist")

    def guard_support_area_not_duplicate(self, support_area_code: str):
        if support_area_code in [a.code for a in self.practice.support_areas]:
            raise ValueError(f"Support area {support_area_code} already exists")

    def guard_funding_source_must_exist(self, funding_source_transit):
        if funding_source_transit not in [f.transit for f in self.practice.funding_sources]:
            raise ValueError(f"Funding source {funding_source_transit} does not exist")

    def guard_consultancy_not_duplicate(self, code: str):
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

    def aggregate_contractors_employees(self) -> List[Person]:
        people: list[Person] = [p for p in self.practice.contractors]
        for p in self.practice.employees:
            people.append(p)
        return people

    def count_business_days_between_dates(self, start_date: date, end_date: date) -> int:
        return pd.bdate_range(start_date, end_date, freq='C', holidays=self.practice.statutory_holiday_list).size

    def find_relevant_transaction_agreement(self, contractor_code: str, on: date):
        candidates = [t for t in self.practice.transaction_agreements if
                      t.contractor_code == contractor_code and t.start_date <= on <= t.end_date]
        if len(candidates) == 0:
            raise ValueError(f"No relevant transaction agreement for contractor {contractor_code} on {on}")
        if len(candidates) > 1:
            raise ValueError(f"Multiple relevant transaction agreements for contractor {contractor_code} on {on}")
        return candidates[0]