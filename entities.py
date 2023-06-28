from datetime import date

from pydantic import BaseModel


class Money(BaseModel):
    __root__: float

    def percent(self, percent: float) -> float:
        return round(self.__root__ * percent, 2)

    def __str__(self):
        return f"${self.__root__:,.2f}"


class FundingSource(BaseModel):
    transit: int
    name: str
    total: Money


class SupportArea(BaseModel):
    code: str
    name: str


class LineItem(BaseModel):
    description: str
    amount: Money
    taxable: bool


class HoursLineItem(LineItem):
    contractor_code: str
    hours: int


class ExpenseLineItem(LineItem):
    pass


class Invoice(BaseModel):
    number: str
    paid: bool = False
    issue_date: date
    period_start: date
    period_end: date
    line_items: list[LineItem] = []

    def total(self) -> Money:
        amounts = [i.amount.__root__ for i in self.line_items]
        total = sum(amounts)
        money = Money(__root__=total)
        return money


class Consultancy(BaseModel):
    code: str
    name: str
    contract: str
    contact_name: str
    contact_phone: str
    contact_email: str
    invoices: list[Invoice] = []


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
    phone_number: str
    email: str
    start_date: date

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
    consultancies: list[Consultancy] = []
    people: list[Person] = []
    transaction_agreements: list[TransactionAgreement] = []
    funding_sources: list[FundingSource] = []
    support_areas: list[SupportArea] = []
    area_assignments: list[AreaAssignment] = []

    @classmethod
    def load(cls):
        return cls.parse_file("practice.json")

    def save(self):
        with open("practice.json", "w") as f:
            f.write(self.json(indent=4))
