from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_employee import AddEmployee


def test_can_add_employee(empty_practice: CoachingPracticeFinance, first_employee_details: dict):
    practice = CoachingPracticeFinance()

    AddEmployee(practice).execute(**first_employee_details)

    verify_model(practice.employees)
