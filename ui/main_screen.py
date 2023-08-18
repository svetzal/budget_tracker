from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QTabWidget, QListWidget, QTableWidget, \
    QTableWidgetItem

from ui.chart_canvas import BudgetAndActualsCanvas


class MainScreen(QWidget):
    def __init__(self, coaching_practice_finance, main_form):
        super().__init__()
        self.main_form = main_form
        self.coaching_practice_finance = coaching_practice_finance

        self.main_layout = QVBoxLayout()

        self.chart_group = QGroupBox("Dashboard")
        charts_layout = QHBoxLayout()
        charts_layout.addWidget(BudgetAndActualsCanvas(self.coaching_practice_finance))
        self.chart_group.setLayout(charts_layout)

        self.main_layout.addWidget(self.chart_group)

        self.data_group = QGroupBox()

        tables_layout = QVBoxLayout()

        self.consultancies_list = self.create_consultancies_table()
        self.contractors_list = self.create_contractors_table()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_consultancies_table(), "Consultancies")
        self.tab_widget.addTab(self.create_contractors_table(), "Contractors")

        tables_layout.addWidget(self.tab_widget)
        self.data_group.setLayout(tables_layout)

        self.main_layout.addWidget(self.data_group)

        self.setLayout(self.main_layout)

    def create_contractors_table(self):
        table = QTableWidget(len(self.coaching_practice_finance.contractors), 3)
        table.setHorizontalHeaderLabels(["Name", "Email", "Start Date"])
        for i, c in enumerate(self.coaching_practice_finance.contractors):
            table.setItem(i, 0, self.create_readonly_item(c.name))
            table.setItem(i, 1, self.create_readonly_item(c.email))
            table.setItem(i, 2, self.create_readonly_item(c.start_date.strftime("%Y-%m-%d")))
        table.setSortingEnabled(True)
        table.resizeColumnsToContents()
        return table

    def create_readonly_item(self, name):
        item = QTableWidgetItem(name)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        return item

    def create_consultancies_table(self):
        table = QTableWidget(len(self.coaching_practice_finance.consultancies), 1)
        table.setHorizontalHeaderLabels(["Name"])
        for i, c in enumerate(self.coaching_practice_finance.consultancies):
            table.setItem(i, 0, self.create_readonly_item(c.name))
        table.setSortingEnabled(True)
        table.resizeColumnsToContents()
        return table
