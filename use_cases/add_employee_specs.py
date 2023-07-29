from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_employee import AddEmployee


def test_can_add_employee():
    practice = CoachingPracticeFinance()
    AddEmployee(practice).execute(
        code="1",
        name="Employee 1",
        email="someone@mycompany.com",
        start_date="2021-01-01"
    )

    verify_model(practice.employees)
