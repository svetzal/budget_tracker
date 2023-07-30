import pandas as pd

from presentation import DataFrameRenderer
from use_cases.use_case import UseCase


class ListTransactionAgreementsByContractor(UseCase):
    def execute(self):
        # Number, Hours, Rate, Start, End
        rows = []
        for c in self.practice.contractors:
            for t in self.practice.transaction_agreements:
                rows.append([c.name, t.number, t.hours, t.rate, t.start_date, t.end_date])
        df = pd.DataFrame(rows, columns=["Contractor", "Number", "Hours", "Rate", "Start", "End"])
        return DataFrameRenderer(title="Transaction Agreements", data=df, sort_by=["Contractor"]).lines()
