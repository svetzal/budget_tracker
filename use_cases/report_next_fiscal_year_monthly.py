from datetime import date

import pandas as pd
from dateutil.relativedelta import relativedelta

from use_cases.use_case import UseCase


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
