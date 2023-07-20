from typing import Optional, List

import pandas as pd
from tabulate import tabulate


class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DataFrameReport:
    title: str
    columns: list[str] = []
    data: pd.DataFrame = None
    sort_by: list[str] = None

    def __init__(self, title: str):
        self.title = title
        self.columns = []
        self.sort_by = None

    def add_column(self, label):
        self.columns.append(label)

    def add_row(self, *args):
        d = dict(zip(self.columns, [[a] for a in args]))
        frame = pd.DataFrame.from_dict(d, orient='columns')
        if self.data is None:
            self.data = frame
        else:
            self.data = pd.concat([self.data, frame])

    def sort(self, columns):
        self.sort_by = columns

    def render(self):
        data = self.data if self.sort_by is None else self.data.sort_values(by=self.sort_by)
        lines: list[str] = []
        lines.append("")
        lines.append(self.title)
        lines.append("")
        lines.append(
            tabulate(
                data,
                headers=[Colours.BOLD + Colours.UNDERLINE + col + Colours.RESET for col in self.columns],
                tablefmt='plain',
                showindex=False
            )
        )
        return lines


class DataFrameRenderer:
    title: str
    data: pd.DataFrame = None
    sort_by: Optional[List[str]] = None

    def __init__(self, title: str, data: pd.DataFrame, sort_by: Optional[List[str]] = None):
        self.title = title
        self.data = data
        self.sort_by = sort_by

    def sort(self, columns: list[str]):
        self.sort_by = columns

    def lines(self):
        data = self.data if self.sort_by is None else self.data.sort_values(by=self.sort_by)
        lines: List[str] = ["", self.title, "", tabulate(
            data,
            headers=[Colours.BOLD + Colours.UNDERLINE + col + Colours.RESET for col in data.columns],
            tablefmt='plain',
            showindex=False
        )]
        return lines

    def __str__(self):
        return "\n".join(self.lines())

class Report:
    ALIGN_RIGHT = '>'
    ALIGN_LEFT = '<'
    ALIGN_CENTER = '^'
    title: str
    columns: list[tuple[str, int, str]] = []
    data: list[tuple] = []

    def __init__(self, title: str):
        self.title = title
        self.columns = []
        self.data = []

    def add_column(self, label, width, align=ALIGN_LEFT):
        self.columns.append((label, width, align))

    def add_row(self, *args):
        self.data.append(args)

    def render(self):
        lines: list[str] = []
        lines.append("")
        lines.append(self.title)
        lines.append("")
        lines.append(self._render_header())
        for row in self.data:
            lines.append(self.render_row(row))
        return lines

    def render_row(self, row):
        return " ".join([f"{str(value):<{width}}" for value, (label, width, align) in zip(row, self.columns)])

    def _render_header(self):
        return " ".join([f"{Colours.BOLD + Colours.UNDERLINE}{label:<{width}}{Colours.RESET}" for label, width, align in
                         self.columns])
