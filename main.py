from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from entities import CoachingPracticeFinance

app = QApplication([])

coaching_practice_finance = CoachingPracticeFinance.load("./practice.json")
main_win = MainWindow(coaching_practice_finance)
main_win.show()

app.exec()