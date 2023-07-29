import datetime
from _decimal import Decimal

from data_types import Money
from entities import TransactionAgreement
from use_cases.use_case import UseCase


class AddTransactionAgreement(UseCase):
    def execute(self, number: str, contractor_code: str, hours: int, rate: float, start_date: str, end_date: str):
        self.guard_contractor_exists(contractor_code)
        self.guard_transaction_agreement_duplicate(number)
        transaction_agreement = TransactionAgreement(
            number=number,
            contractor_code=contractor_code,
            hours=hours,
            rate=Money(root=Decimal(rate)),
            start_date=datetime.date.fromisoformat(start_date),
            end_date=datetime.date.fromisoformat(end_date)
        )
        self.practice.transaction_agreements.append(transaction_agreement)
