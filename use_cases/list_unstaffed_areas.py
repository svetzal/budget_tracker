import pandas as pd
from tabulate import tabulate

from use_cases.use_case import UseCase


class ListUnstaffedAreas(UseCase):
    def execute(self, start_date: str, end_date: str):
        period_start = pd.to_datetime(start_date)
        period_end = pd.to_datetime(end_date)

        report_date_range = pd.bdate_range(period_start, period_end, freq="C",
                                           holidays=self.practice.statutory_holiday_list)
        report_frame = pd.DataFrame(report_date_range, columns=["date"])
        assignments_frame = self.prepare_assignments_frame(report_date_range)
        report_frame = report_frame.merge(assignments_frame, how="outer", on="date")
        self.prepare_date_groupings(report_frame)
        lines = self.prepare_report_output(report_frame)
        return lines

    def prepare_report_output(self, report_frame):
        lines = []
        for a in self.practice.support_areas:
            unstaffed = report_frame[report_frame[a.code] == False]
            report = unstaffed.groupby(f"{a.code}_group")['date'].agg(['min', 'max'])
            report = report.reset_index(drop=True)
            if report.count()[0] > 0:
                lines.append("")
                lines.append(f"{self.find_support_area(a.code).name} is Unstaffed")
                lines.append("")
                report['min'] = report['min'].dt.strftime('%Y-%m-%d')
                report['max'] = report['max'].dt.strftime('%Y-%m-%d')
                report.columns = ['Start Date', 'End Date']
                lines.append(tabulate(report, showindex=False, tablefmt='plain'))
        return lines

    def prepare_date_groupings(self, report_frame):
        for a in self.practice.support_areas:
            report_frame[f"{a.code}_group"] = (report_frame[a.code].diff() != 0).cumsum()

    def prepare_assignments_frame(self, report_date_range):
        assignment_coverage = []
        columns = ['date'] + [a.code for a in self.practice.support_areas]
        for date in report_date_range:
            row = [date]
            for a in self.practice.support_areas:
                covered = False
                for aa in self.practice.area_assignments:
                    if aa.support_area_code == a.code:
                        start = pd.to_datetime(aa.start_date)
                        end = pd.to_datetime(aa.end_date)
                        if start <= date <= end:
                            covered = True
                row.append(covered)
            assignment_coverage.append(row)
        assignments_frame = pd.DataFrame(assignment_coverage, columns=columns)
        return assignments_frame


