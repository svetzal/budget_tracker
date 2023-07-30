from _decimal import Decimal

from pydantic import RootModel


class Money(RootModel):
    root: Decimal

    @classmethod
    def from_float(cls, value: float) -> 'Money':
        return cls(root=Decimal(value))

    @classmethod
    def from_int(cls, value: int) -> 'Money':
        return cls(root=Decimal(value))

    def percent(self, percent: float) -> Decimal:
        return Decimal(round(float(self.root) * percent, 2))

    def __str__(self):
        return f"${self.root:,.2f}"
