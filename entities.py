from decimal import Decimal
from datetime import date
from typing import Literal, Union, Optional, List

from pydantic import BaseModel, Field

from data_types import Money


class FundingSource(BaseModel):
    transit: int = Field(..., description="Transit number of the funding source")
    name: str = Field(..., description="Name of the funding source")
    total: Money = Field(..., description="Total funds in the funding source")
    start_date: date = Field(..., description="Start date of the funding source")
    end_date: date = Field(..., description="End date of the funding source")


class SupportArea(BaseModel):
    code: str = Field(..., description="Code of the support area")
    name: str = Field(..., description="Name of the support area")


class CoachAssessment(BaseModel):
    completed_on: date = Field(..., description="Date the coach assessment was completed")
    leadership: float = Field(..., description="Leadership score of the coach profile")
    technical: float = Field(..., description="Technical score of the coach profile")
    practice: float = Field(..., description="Practice score of the coach profile")


class SupportPlan(BaseModel):
    support_area_code: str = Field(..., description="Support area of the support plan")
    contractor_code: str = Field(..., description="Contractor code of the support plan")
    start_date: date = Field(..., description="Start date of the support plan")
    end_date: date = Field(..., description="End date of the support plan")
    coach_profile: CoachAssessment = Field(..., description="Coach profile of the support plan")

class LineItem(BaseModel):
    description: str = Field(..., description="Description of the line item")
    amount: Money = Field(..., description="Amount of the line item")
    taxable: bool = Field(..., description="Taxable status of the line item")


class HoursLineItem(LineItem):
    contractor_code: str = Field(..., description="Contractor code of the line item")
    hours: Optional[float] = Field(None, description="Number of hours for the line item")
    period_start: date = Field(..., description="Start date of the period covered by the line item")
    period_end: date = Field(..., description="End date of the period covered by the line item")
    tag: Literal["Hours"] = "Hours"


class ExpenseLineItem(LineItem):
    contractor_code: str = Field(..., description="Contractor code of the line item")
    tag: Literal["Expense"] = "Expense"


class IncidentalLineItem(LineItem):
    tag: Literal["Incidental"] = "Incidental"


class Invoice(BaseModel):
    number: str = Field(..., description="Number of the invoice")
    paid_date: Optional[date] = Field(None, description="Date invoice was paid")
    issue_date: date = Field(..., description="Issue date of the invoice")
    line_items: List[Union[IncidentalLineItem, HoursLineItem, ExpenseLineItem]] = []

    def total(self) -> Money:
        amounts = [i.amount.root for i in self.line_items]
        total = sum(amounts)
        money = Money(root=total)
        return money


class Consultancy(BaseModel):
    code: str = Field(..., description="Code of the consultancy")
    name: str = Field(..., description="Name of the consultancy")
    contract: str = Field(..., description="Contract of the consultancy")
    contact_name: str = Field(..., description="Contact name for the consultancy")
    contact_phone: Optional[str] = Field(None, description="Contact phone for the consultancy")
    contact_email: Optional[str] = Field(None, description="Contact email for the consultancy")
    invoices: List[Invoice] = []


class TransactionAgreement(BaseModel):
    number: str = Field(..., description="Number of the transaction agreement")
    contractor_code: str = Field(..., description="Contractor code of the transaction agreement")
    hours: int = Field(..., description="Number of hours in the transaction agreement")
    rate: Money = Field(..., description="Rate of the transaction agreement")
    start_date: date = Field(..., description="Start date of the transaction agreement")
    end_date: date = Field(..., description="End date of the transaction agreement")


class Person(BaseModel):
    code: str = Field(..., description="Code of the person")
    name: str = Field(..., description="Name of the person")
    email: str = Field(..., description="Email of the person")
    start_date: date = Field(..., description="Start date of employment for the person")
    phone_number: Optional[str] = Field(None, description="Phone number of the person")
    end_date: Optional[date] = Field(None, description="End date of employment for the person")
    assessments: List[CoachAssessment] = []

    def org_code(self):
        return None

    def works_through(self, consultancy_code: str) -> bool:
        return False


class Employee(Person):
    pass


class Contractor(Person):
    consultancy_code: str = Field(..., description="Consultancy code of the contractor")

    def org_code(self):
        return self.consultancy_code

    def works_through(self, consultancy_code: str) -> bool:
        return self.consultancy_code == consultancy_code


class AreaAssignment(BaseModel):
    support_area_code: str = Field(..., description="Support area code of the area assignment")
    contractor_code: str = Field(..., description="Contractor code of the area assignment")
    funding_source_transit: int = Field(..., description="Funding source transit of the area assignment")
    start_date: date = Field(..., description="Start date of the area assignment")
    end_date: date = Field(..., description="End date of the area assignment")


class CoachingPracticeFinance(BaseModel):
    fiscal_start_month: int = Field(11, description="Start month of the fiscal year")
    stat_holidays_per_year: int = Field(9, description="Number of statutory holidays per year")
    statutory_holiday_list: List[str] = ['2023-01-02', '2023-02-20', '2023-04-07', '2023-05-22', '2023-07-03',
                                         '2023-08-07', '2023-09-04', '2023-10-09', '2023-12-25', '2023-12-26',
                                         '2024-01-01', '2024-02-19', '2024-04-01', '2024-05-20', '2024-07-01',
                                         '2024-08-05', '2024-09-02', '2024-10-14', '2024-12-25', '2024-12-26']
    expected_weeks_holidays: int = Field(4, description="Number of expected weeks of holidays")
    standard_hours_per_day: Decimal = Field(7.5, description="Standard hours per day")
    consultancies: List[Consultancy] = []
    employees: List[Employee] = []
    contractors: List[Contractor] = []
    transaction_agreements: List[TransactionAgreement] = []
    funding_sources: List[FundingSource] = []
    support_areas: List[SupportArea] = []
    support_plans: List[SupportPlan] = []
    area_assignments: List[AreaAssignment] = []

    @classmethod
    def load(cls, filename: str = "practice.json"):
        with open(filename, "r") as f:
            return cls.model_validate_json(f.read())

    def save(self, filename: str = "practice.json"):
        with open(filename, "w") as f:
            f.write(self.model_dump_json(indent=4))
