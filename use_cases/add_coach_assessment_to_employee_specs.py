from entities import CoachingPracticeFinance
from use_cases.add_coach_assessment_to_employee import AddCoachAssessmentToEmployee
from use_cases.test_data_generators import FIRST_EMPLOYEE_CODE
from verifiers import verify_model


def test_can_add_coach_assessment_to_employee(staffed_practice: CoachingPracticeFinance):
    AddCoachAssessmentToEmployee(staffed_practice).execute(
        employee_code=FIRST_EMPLOYEE_CODE,
        completed_on="2023-01-01",
        leadership=0.5,
        technical=0.5,
        practice=1.0,
    )

    verify_model(staffed_practice.employees)
