from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QTabWidget, QListWidget

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

        self.tab_widget = QTabWidget()
        self.consultancies_list = QListWidget()
        self.contractors_list = QListWidget()
        self.tab_widget.addTab(self.consultancies_list, "Consultancies")
        self.tab_widget.addTab(self.contractors_list, "Contractors")

        tables_layout.addWidget(self.tab_widget)
        self.data_group.setLayout(tables_layout)

        self.main_layout.addWidget(self.data_group)

        self.setLayout(self.main_layout)
