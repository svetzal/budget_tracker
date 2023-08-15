from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton

from use_cases.add_consultancy import AddConsultancy


class ConsultancyForm(QWidget):
    def __init__(self, coaching_practice_finance, main_form):
        super().__init__()
        self.main_form = main_form
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
        self.main_form.show_main_layout()
