from datetime import date

from dateutil.relativedelta import relativedelta

from presentation import Report
from use_cases.use_case import UseCase


class CurrentFiscalYearMonthly(UseCase):

    def execute(self):
        current_year = date.today().year
        report = Report(f"FY{current_year} Monthly")
        report.add_column("Month", 10)
        report.add_column("Invoice #", 15)
        report.add_column("Billing Days", 15)
        report.add_column("Amount", 11)
        report.add_column("Paid", 6)
        report.add_column("Budget", 11)

        fiscal_start = date(current_year - 1, self.practice.fiscal_start_month, 1)
        for month in range(0, 12):
            month_start = fiscal_start + relativedelta(months=month)
            month_end = fiscal_start + relativedelta(months=month + 1) - relativedelta(days=1)

            invoices = [i for c in self.practice.consultancies for i in c.invoices]
            for i in invoices:
                overlap_start, overlap_end = self.calculate_overlap(i, month_end, month_start)
                if overlap_start is not None:
                    billing_days = self.count_business_days_between_dates(i.period_start, i.period_end)
                    overlap_days = self.count_business_days_between_dates(overlap_start, overlap_end)
                    report.add_row(
                        month_start.strftime("%b"),
                        i.number,
                        overlap_days,
                        i.total().percent(overlap_days / billing_days),
                        "✔︎" if i.paid else ""
                    )

        return report.render()

    def calculate_overlap(self, invoice, month_end, month_start):
        # Move this to calculate the intersection of two date ranges
        overlap_start = None
        overlap_end = None
        if invoice.period_end <= month_start:
            # invoice period is before month
            return None, None
        if invoice.period_start >= month_end:
            # invoice period is after month
            return None, None
        if invoice.period_start <= month_start and invoice.period_end >= month_end:
            # invoice period is entirely within month
            overlap_start = month_start
            overlap_end = month_end
        if invoice.period_start >= month_start and invoice.period_end <= month_end:
            # month is entirely within invoice period
            overlap_start = invoice.period_start
            overlap_end = invoice.period_end
        if invoice.period_start <= month_start and invoice.period_end <= month_end:
            # invoice period starts before month but ends within month
            overlap_start = month_start
            overlap_end = invoice.period_end
        if invoice.period_start >= month_start and invoice.period_end >= month_end:
            # invoice period starts within month but ends after month
            overlap_start = invoice.period_start
            overlap_end = month_end
        return overlap_start, overlap_end
