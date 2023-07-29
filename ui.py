from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFormLayout, QLineEdit, \
    QLabel, QComboBox, QListWidget
from PyQt6.QtCore import Qt
from use_cases.add_contractor import AddContractor
from use_cases.add_consultancy import AddConsultancy


class MainWindow(QMainWindow):
    def __init__(self, coaching_practice_finance):
        super().__init__()

        self.coaching_practice_finance = coaching_practice_finance
        self.setWindowTitle("Coaching Practice Finance")

        self.main_layout = QVBoxLayout()
        self.consultancies_list = QListWidget()
        self.contractors_list = QListWidget()

        self.main_layout.addWidget(QLabel("Consultancies:"))
        self.main_layout.addWidget(self.consultancies_list)
        self.main_layout.addWidget(QLabel("Contractors:"))
        self.main_layout.addWidget(self.contractors_list)

        self.add_consultancy_button = QPushButton("Add Consultancy")
        self.add_consultancy_button.clicked.connect(self.on_add_consultancy)

        self.add_contractor_button = QPushButton("Add Contractor")
        self.add_contractor_button.clicked.connect(self.on_add_contractor)

        self.main_layout.addWidget(self.add_consultancy_button)
        self.main_layout.addWidget(self.add_contractor_button)

        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

    def on_add_consultancy(self):
        self.consultancy_form = ConsultancyForm(self.coaching_practice_finance)
        self.setCentralWidget(self.consultancy_form)

    def on_add_contractor(self):
        self.contractor_form = ContractorForm(self.coaching_practice_finance)
        self.setCentralWidget(self.contractor_form)


class ConsultancyForm(QWidget):
    def __init__(self, coaching_practice_finance):
        super().__init__()

        self.coaching_practice_finance = coaching_practice_finance

        self.form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()

        self.form_layout.addRow('ID:', self.id_input)
        self.form_layout.addRow('Name:', self.name_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_consultancy)
        self.form_layout.addWidget(self.submit_button)

        self.setLayout(self.form_layout)

    def submit_consultancy(self):
        id_text = self.id_input.text()
        name_text = self.name_input.text()

        add_consultancy_use_case = AddConsultancy(self.coaching_practice_finance)
        # add_consultancy_use_case.execute(id_text, name_text)


class ContractorForm(QWidget):
    def __init__(self, coaching_practice_finance):
        super().__init__()

        self.coaching_practice_finance = coaching_practice_finance

        self.form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.consultancy_id_input = QLineEdit()

        self.form_layout.addRow('ID:', self.id_input)
        self.form_layout.addRow('Name:', self.name_input)
        self.form_layout.addRow('Consultancy ID:', self.consultancy_id_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_contractor)
        self.form_layout.addWidget(self.submit_button)

        self.setLayout(self.form_layout)

    def submit_contractor(self):
        id_text = self.id_input.text()
        name_text = self.name_input.text()
        consultancy_id_text = self.consultancy_id_input.text()

        add_contractor_use_case = AddContractor(self.coaching_practice_finance)
        # add_contractor_use_case.execute(id_text, name_text, consultancy_id_text)