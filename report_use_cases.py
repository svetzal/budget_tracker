import pandas as pd

from datetime import date
from dateutil.relativedelta import *

from entities import Person
from presentation import Report, DataFrameReport, DataFrameRenderer
from use_cases import UseCase


class ListAreas(UseCase):
    def execute(self):
        areas = []
        for c in self.practice.contractors:
            for a in self.practice.support_areas:
                for s in self.practice.area_assignments:
                    if c.code == s.contractor_code and s.support_area_code == a.code:
                        areas.append([a.name, c.name, s.funding_source_transit, s.start_date, s.end_date])
        df = pd.DataFrame(areas, columns=["Area", "Contractor", "Funding Source", "Start Date", "End Date"])
        output = DataFrameRenderer(title="Area Assignments", data=df, sort_by=["Area", "Contractor"])
        return output.lines()


class ListUnpaidInvoices(UseCase):
    def execute(self):
        invoices = []
        for c in self.practice.consultancies:
            for i in c.invoices:
                invoices.append([i.number, i.issue_date.isoformat(), i.total(), c.name, i.paid])
        df = pd.DataFrame(invoices, columns=["Invoice Number", "Issue Date", "Total", "Consultancy", "Paid"])
        output = DataFrameRenderer(title="Invoices", data=df, sort_by=["Issue Date", "Invoice Number"])
        return output.lines()


class ListPeople(UseCase):
    def execute(self):
        people = []
        for c in self.practice.consultancies:
            for p in self.practice.contractors:
                if c.code == p.consultancy_code:
                    people.append([p.code, p.name, c.name])
        for p in self.practice.employees:
            people.append([p.code, p.name, "RBC"])
        df = pd.DataFrame(people, columns=["Code", "Name", "Company"])
        output = DataFrameRenderer(title="People", data=df, sort_by=["Name"])
        return output.lines()


class ListContractors(UseCase):
    def execute(self):
        contractors = []
        for consultancy in self.practice.consultancies:
            for c in self.practice.contractors:
                if c.consultancy_code == consultancy.code:
                    ta_found = False
                    for ta in self.practice.transaction_agreements:
                        if ta.contractor_code == c.code:
                            if ta.start_date <= date.today() <= ta.end_date:
                                ta_found = True
                                contractors.append(
                                    [c.code, c.name, consultancy.name, ta.number, ta.rate, ta.hours, ta.start_date,
                                     ta.end_date])
                    if not ta_found:
                        contractors.append([c.code, c.name, consultancy.name, None, None, "", None, None])
        df = pd.DataFrame(contractors,
                          columns=["Code", "Name", "Consultancy", "Agreement", "Rate", "Hours", "Start", "End"])
        output = DataFrameRenderer(title="Contractors", data=df, sort_by=["Name"])
        return output.lines()


class ListConsultancies(UseCase):
    def execute(self):
        consultancies = []
        for o in self.practice.consultancies:
            for c in self.practice.contractors:
                if o.code == c.consultancy_code:
                    consultancies.append([o.code, o.name, c.code])
        df = pd.DataFrame(consultancies, columns=["Code", "Name", "Contractors"])
        aggregated = df.groupby(["Code", "Name"], as_index=False).count()
        output = DataFrameRenderer(title="Consultancies", data=aggregated, sort_by=["Name"])
        return output.lines()


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


class NextFiscalYearBudgetMonthly(UseCase):

    def execute(self):
        current_year = date.today().year
        report_date_range = self.calculate_fiscal_year_range(current_year + 1)

        rows = []
        for ta in self.practice.transaction_agreements:
            ta_range = pd.bdate_range(ta.start_date, ta.end_date, freq="C",
                                      holidays=self.practice.statutory_holiday_list)
            for day in ta_range:
                ta_dict = ta.__dict__.copy()
                ta_dict["rate"] = float(ta.rate.__root__)
                ta_dict["date"] = day
                ta_dict["hours"] = float(self.practice.standard_hours_per_day)
                rows.append(ta_dict)

        budget_frame = pd.DataFrame(rows)
        budget_frame["amount"] = budget_frame.rate * budget_frame.hours
        budget_frame["month"] = budget_frame.date.dt.month

        rows = []
        for consultancy in self.practice.consultancies:
            for invoice in consultancy.invoices:
                for line_item in invoice.line_items:
                    line_item_dict = line_item.dict()
                    line_item_dict["type"] = line_item.__class__.__name__
                    line_item_dict["amount"] = float(line_item.amount.__root__)
                    if line_item_dict["type"] == ExpenseLineItem.__name__:
                        line_item_dict["date"] = pd.Timestamp(invoice.period_start)
                        rows.append(line_item_dict)
                    else:
                        hours_range = pd.bdate_range(invoice.period_start, invoice.period_end, freq="C",
                                                     holidays=practice.statutory_holiday_list)
                        days = len(hours_range)
                        daily_hours = line_item_dict["hours"] / days
                        daily_amount = line_item_dict["amount"] / days
                        for day in hours_range:
                            dated_dict = line_item_dict.copy()
                            dated_dict["date"] = day
                            dated_dict["amount"] = daily_amount
                            dated_dict["hours"] = daily_hours
                            rows.append(dated_dict)
        # rows
        actuals_frame = pd.DataFrame(rows)
        actuals_frame["month"] = actuals_frame.date.dt.month

        merged = budget_frame[["date", "amount", "month"]].merge(actuals_frame[["date", "amount"]], on="date",
                                                                 how='outer')
        merged.columns = ["date", "budget", "month", "actual"]
        # merged["actual"] = merged["actual"].fillna(0)
        merged[["month", "budget", "actual"]].groupby("month").sum()

    def calculate_fiscal_year_range(self, fiscal_year):
        fiscal_start = date(fiscal_year, 1, 1) \
            if self.practice.fiscal_start_month == 1 \
            else date(fiscal_year - 1, self.practice.fiscal_start_month, 1)
        fiscal_end = fiscal_start + relativedelta(years=1) - relativedelta(days=1)
        return pd.date_range(fiscal_start, fiscal_end)
