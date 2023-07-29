from entities import CoachingPracticeFinance
from use_cases.list_areas import ListAreas
from verifiers import verify_report


def test_can_list_areas(operational_practice: CoachingPracticeFinance):
    output = ListAreas(operational_practice).execute()

    verify_report(output)
