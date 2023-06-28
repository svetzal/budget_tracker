from datetime import date
from dateutil.relativedelta import *

from entities import Person
from report import Report
from use_cases import UseCase


class ListAreas(UseCase):
    def execute(self):
        report = Report("Supported Areas")
        report.add_column("Support Area", 13)
        report.add_column("Funding Source", 15)
        report.add_column("Contractor", 30)
        for a in self.practice.area_assignments:
            report.add_row(a.support_area_code, a.funding_source_transit, self.find_contractor(a.contractor_code).name)
        return report.render()


class ListUnpaidInvoices(UseCase):
    def execute(self):
        report = Report("Unpaid Invoices")
        report.add_column("Number", 8)
        report.add_column("Issued", 10)
        report.add_column("Consultancy", 30)
        report.add_column("Amount", 8)
        invoices = [i for c in self.practice.consultancies for i in c.invoices if not i.paid]
        for i in invoices:
            report.add_row(i.number, i.issue_date.isoformat(), self.find_consultancy_by_invoice(i.number).name,
                           str(i.total()))
        return report.render()


class ListPeople(UseCase):
    def organization_name(self, person: Person):
        consultancy = self.find_consultancy_by_code(person.org_code())
        return consultancy.name if consultancy else ""

    def execute(self):
        report = Report("Contractors")
        report.add_column("Code", 8)
        report.add_column("Name", 30)
        report.add_column("Organization", 20)
        for p in self.practice.people:
            report.add_row(p.code, p.name, self.organization_name(p))
        return report.render()


class ListConsultancies(UseCase):
    def count_contractors(self, consultancy_code: str):
        return len([p for p in self.practice.people if p.works_through(consultancy_code)])

    def execute(self):
        report = Report("Consultancies")
        report.add_column("Code", 8)
        report.add_column("Name", 30)
        report.add_column("Size", 5)
        for c in self.practice.consultancies:
            report.add_row(c.code, c.name, self.count_contractors(c.code))
        return report.render()


class CurrentFiscalYearMonthly(UseCase):
    fiscal_start: int = 11

    def execute(self):
        current_year = date.today().year
        report = Report(f"FY{current_year} Monthly")
        report.add_column("Month", 10)
        report.add_column("Invoice #", 15)
        report.add_column("Billing Days", 15)
        report.add_column("Amount", 11)
        report.add_column("Paid", 6)

        fiscal_start = date(current_year - 1, self.fiscal_start, 1)
        for month in range(0, 12):
            month_start = fiscal_start + relativedelta(months=month)
            month_end = fiscal_start + relativedelta(months=month + 1) - relativedelta(days=1)

            invoices = [i for c in self.practice.consultancies for i in c.invoices]
            for i in invoices:
                overlap_start, overlap_end = self.calculate_overlap(i, month_end, month_start)
                if overlap_start is not None:
                    billing_days = self.calculate_working_days(i.period_start, i.period_end)
                    overlap_days = self.calculate_working_days(overlap_start, overlap_end)
                    report.add_row(
                        month_start.strftime("%b"),
                        i.number,
                        overlap_days,
                        i.total().percent(overlap_days / billing_days),
                        "✔︎" if i.paid else ""
                    )

        return report.render()

    def calculate_working_days(self, period_start: date, period_end: date) -> int:
        working_days = 0
        for day in range(0, (period_end - period_start).days + 1):
            if (period_start + relativedelta(days=day)).weekday() < 5:
                working_days += 1
        return working_days

    def calculate_overlap(self, invoice, month_end, month_start):
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
