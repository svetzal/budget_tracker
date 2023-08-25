import pandas as pd
from PyQt6 import QtCore
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class ChartWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self, practice):
        super().__init__()
        self.practice = practice

    def run(self):
        period_start = pd.to_datetime("2022-11-01")
        period_end = pd.to_datetime("2023-10-31")
        report_date_range = pd.bdate_range(period_start, period_end, freq="C", holidays=self.practice.statutory_holiday_list)
        report_frame = pd.DataFrame(report_date_range, columns=["date"])

        ta_array = []
        for ta in self.practice.transaction_agreements:
            ta_range = pd.bdate_range(ta.start_date, ta.end_date, freq="C", holidays=self.practice.statutory_holiday_list)
            for date in ta_range:
                if date in report_date_range:
                    ta_dict = ta.model_dump()
                    ta_dict["rate"] = float(ta.rate.root)
                    ta_dict["date"] = date
                    ta_dict["hours"] = float(ta.hours / len(ta_range))
                    ta_array.append(ta_dict)

        ta_frame = pd.DataFrame(ta_array)
        ta_frame["amount"] = ta_frame.rate * ta_frame.hours

        budget_summary = ta_frame[["date", "amount"]].rename(columns={"amount": "budget"})
        budget_summary = budget_summary.groupby("date").sum()

        report_frame = report_frame.merge(budget_summary, on=["date"], how="outer")

        ta_array = []
        for consultancy in self.practice.consultancies:
            for invoice in consultancy.invoices:
                for line_item in invoice.line_items:
                    line_item_dict = line_item.model_dump()
                    line_item_dict["amount"] = float(line_item.amount.root)
                    if line_item_dict["tag"] == "Hours":
                        hours_range = pd.bdate_range(line_item.period_start, line_item.period_end, freq="C",
                                                     holidays=self.practice.statutory_holiday_list)
                        days = len(hours_range)
                        daily_hours = line_item_dict["hours"] / days
                        daily_amount = line_item_dict["amount"] / days
                        for date in hours_range:
                            dated_dict = line_item_dict.copy()
                            dated_dict["date"] = date
                            dated_dict["amount"] = daily_amount
                            dated_dict["hours"] = daily_hours
                            ta_array.append(dated_dict)
                    else:
                        line_item_dict["date"] = pd.Timestamp(invoice.issue_date)
                        ta_array.append(line_item_dict)
        actuals_frame = pd.DataFrame(ta_array)

        actuals_summary = actuals_frame[["date", "amount"]].rename(columns={"amount": "actual"})
        actuals_summary = actuals_summary.groupby("date").sum()

        report_frame = report_frame.merge(actuals_summary, on="date", how='outer')

        report_frame['year'] = report_frame['date'].dt.year
        report_frame['month'] = report_frame['date'].dt.month
        report_frame['budget'] = report_frame['budget'].fillna(0)
        report_frame['actual'] = report_frame['actual'].fillna(0)
        self.report_frame = report_frame.groupby(["year", "month"]).aggregate({"date": "first", "budget": "sum", "actual": "sum"})

        self.finished.emit()

class BudgetAndActualsCanvas(FigureCanvasQTAgg):
    def __init__(self, practice):
        self.practice = practice
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        super().__init__(fig)
        self.worker = ChartWorker(practice)
        self.worker.finished.connect(self.plot)
        self.worker.start()

    def plot(self):
        self.worker.report_frame.plot(ax=self.ax, y=["budget", "actual"], x='date')
        self.ax.set_title("Budget and Actuals")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Amount")
        self.ax.legend(["Budget", "Actual"])
        self.draw()