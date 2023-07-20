from _decimal import Decimal

from pydantic import BaseModel


class Money(BaseModel):
    root: Decimal

    def percent(self, percent: float) -> Decimal:
        return Decimal(round(float(self.root) * percent, 2))

    def __str__(self):
        return f"${self.root:,.2f}"
