import pandas as pd

from presentation import DataFrameRenderer
from use_cases.use_case import UseCase


class ListUnpaidInvoices(UseCase):
    def execute(self):
        invoices = []
        for c in self.practice.consultancies:
            for i in c.invoices:
                if not i.paid_date:
                    invoices.append([i.number, i.issue_date.isoformat(), i.total(), c.name])
        df = pd.DataFrame(invoices, columns=["Invoice Number", "Issue Date", "Total", "Consultancy"])
        output = DataFrameRenderer(title="Invoices", data=df, sort_by=["Issue Date", "Invoice Number"])
        return output.lines()
