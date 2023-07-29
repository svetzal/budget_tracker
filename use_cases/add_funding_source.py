import datetime
from _decimal import Decimal

from data_types import Money
from entities import FundingSource
from use_cases.use_case import UseCase


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
