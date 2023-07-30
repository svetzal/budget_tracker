from entities import CoachingPracticeFinance
from verifiers import verify_model
from use_cases.add_area_assignment import AddAreaAssignment
from use_cases.test_data_generators import FIRST_SUPPORT_AREA_CODE, FIRST_CONTRACTOR_CODE, FIRST_TRANSIT


def test_add_area_assignment(staffed_practice: CoachingPracticeFinance):
    AddAreaAssignment(staffed_practice).execute(
        support_area_code=FIRST_SUPPORT_AREA_CODE,
        person_code=FIRST_CONTRACTOR_CODE,
        funding_source_transit=FIRST_TRANSIT,
        start_date="2023-01-01",
        end_date="2023-12-31",
    )

    verify_model(staffed_practice.area_assignments)
