from entities import CoachingPracticeFinance
from use_cases.add_coach_assessment_to_contractor import AddCoachAssessmentToContractor
from use_cases.test_data_generators import FIRST_CONTRACTOR_CODE
from verifiers import verify_model


def test_can_add_coach_assessment_to_contractor(staffed_practice: CoachingPracticeFinance):
    AddCoachAssessmentToContractor(staffed_practice).execute(
        contractor_code=FIRST_CONTRACTOR_CODE,
        completed_on="2023-01-01",
        leadership=0.5,
        technical=0.5,
        practice=1.0,
    )

    verify_model(staffed_practice.contractors)
