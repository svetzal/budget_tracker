from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QComboBox

from use_cases.add_contractor import AddContractor


class ContractorForm(QWidget):
    def __init__(self, coaching_practice_finance, main_form):
        super().__init__()
        self.main_form = main_form
        self.coaching_practice_finance = coaching_practice_finance

        self.form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.consultancy_id_input = QComboBox()
        for c in self.coaching_practice_finance.consultancies:
            self.consultancy_id_input.addItem(c.name, c.code)

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
        consultancy_id_text = self.consultancy_id_input.currentData()

        add_contractor_use_case = AddContractor(self.coaching_practice_finance)
        # add_contractor_use_case.execute(id_text, name_text, consultancy_id_text)
        self.main_form.show_main_layout()
