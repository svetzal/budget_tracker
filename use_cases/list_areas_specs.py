from entities import CoachingPracticeFinance, AreaAssignment
from use_cases.test_data_generators import FIRST_SUPPORT_AREA_CODE, FIRST_CONTRACTOR_CODE, FIRST_TRANSIT
from verifiers import verify_report
from use_cases.list_areas import ListAreas


def test_can_list_areas(staffed_assigned_practice: CoachingPracticeFinance):
    output = ListAreas(staffed_assigned_practice).execute()

    verify_report(output)
