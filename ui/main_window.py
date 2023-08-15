from PyQt6.QtWidgets import QMainWindow

from ui.consultancy_form import ConsultancyForm
from ui.contractor_form import ContractorForm
from ui.main_screen import MainScreen


class MainWindow(QMainWindow):
    def __init__(self, coaching_practice_finance):
        super().__init__()

        self.coaching_practice_finance = coaching_practice_finance
        self.show_main_layout()

        menu_bar = self.menuBar()
        contractor_menu = menu_bar.addMenu("Contractors")
        add_contractor_action = contractor_menu.addAction("Add Contractor")
        add_contractor_action.triggered.connect(self.on_add_contractor)

        consultancy_menu = menu_bar.addMenu("Consultancies")
        add_consultancy_action = consultancy_menu.addAction("Add Consultancy")
        add_consultancy_action.triggered.connect(self.on_add_consultancy)

    def show_main_layout(self):
        self.setWindowTitle("Coaching Practice Finance")
        main_screen = MainScreen(self.coaching_practice_finance, self)
        self.setCentralWidget(main_screen)

    def on_add_consultancy(self):
        self.setWindowTitle("Add Consultancy")
        consultancy_form = ConsultancyForm(self.coaching_practice_finance, self)
        self.setCentralWidget(consultancy_form)

    def on_add_contractor(self):
        self.setWindowTitle("Add Contractor")
        contractor_form = ContractorForm(self.coaching_practice_finance, self)
        self.setCentralWidget(contractor_form)
