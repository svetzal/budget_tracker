from decimal import Decimal
from datetime import date
from typing import Literal, Union, Optional

from pydantic import BaseModel
from pydantic.types import List

from data_types import Money


class FundingSource(BaseModel):
    transit: int
    name: str
    total: Money
    start_date: date
    end_date: date


class SupportArea(BaseModel):
    code: str
    name: str


class LineItem(BaseModel):
    description: str
    amount: Money
    contractor_code: str
    taxable: bool


class HoursLineItem(LineItem):
    hours: Optional[int] = None
    tag: Literal["Hours"] = "Hours"


class ExpenseLineItem(LineItem):
    tag: Literal["Expense"] = "Expense"


class IncidentalLineItem(LineItem):
    tag: Literal["Incidental"] = "Incidental"


class Invoice(BaseModel):
    number: str
    paid: bool = False
    issue_date: date
    period_start: date
    period_end: date
    line_items: List[Union[IncidentalLineItem, HoursLineItem, ExpenseLineItem]] = []

    def total(self) -> Money:
        amounts = [i.amount.root for i in self.line_items]
        total = sum(amounts)
        money = Money(root=total)
        return money


class Consultancy(BaseModel):
    code: str
    name: str
    contract: str
    contact_name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    invoices: List[Invoice] = []


class TransactionAgreement(BaseModel):
    number: str
    contractor_code: str
    hours: int
    rate: Money
    start_date: date
    end_date: date


class Person(BaseModel):
    code: str
    name: str
    email: str
    start_date: date
    phone_number: Optional[str] = None
    end_date: Optional[date] = None

    def org_code(self):
        return None

    def works_through(self, consultancy_code: str) -> bool:
        return False


class Employee(Person):
    pass


class Contractor(Person):
    consultancy_code: str

    def org_code(self):
        return self.consultancy_code

    def works_through(self, consultancy_code: str) -> bool:
        return self.consultancy_code == consultancy_code


class AreaAssignment(BaseModel):
    support_area_code: str
    contractor_code: str
    funding_source_transit: int
    start_date: date
    end_date: date


class CoachingPracticeFinance(BaseModel):
    fiscal_start_month: int = 11
    stat_holidays_per_year: int = 9
    statutory_holiday_list: List[str] = ['2023-01-02', '2023-02-20', '2023-04-07', '2023-05-22', '2023-07-03',
                                         '2023-08-07', '2023-09-04', '2023-10-09', '2023-12-25', '2023-12-26',
                                         '2024-01-01', '2024-02-19', '2024-04-01', '2024-05-20', '2024-07-01',
                                         '2024-08-05', '2024-09-02', '2024-10-14', '2024-12-25', '2024-12-26']
    expected_weeks_holidays: int = 4
    standard_hours_per_day: Decimal = 7.5
    consultancies: List[Consultancy] = []
    employees: List[Employee] = []
    contractors: List[Contractor] = []
    transaction_agreements: List[TransactionAgreement] = []
    funding_sources: List[FundingSource] = []
    support_areas: List[SupportArea] = []
    area_assignments: List[AreaAssignment] = []

    @classmethod
    def load(cls):
        with open("practice.json", "r") as f:
            return cls.model_validate_json(f.read())

    def save(self):
        with open("practice.json", "w") as f:
            f.write(self.model_dump_json(indent=4))
