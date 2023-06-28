from presentation import Colours


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
        return " ".join([f"{Colours.BOLD + Colours.UNDERLINE}{label:<{width}}{Colours.RESET}" for label, width, align in self.columns])
