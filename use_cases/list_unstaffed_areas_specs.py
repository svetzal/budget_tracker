from entities import CoachingPracticeFinance
from use_cases.list_unstaffed_areas import ListUnstaffedAreas
from verifiers import verify_report


def test_list_unstaffed_areas(operational_practice: CoachingPracticeFinance):
    output = ListUnstaffedAreas(operational_practice).execute(start_date="2022-11-01", end_date="2023-10-31")

    verify_report(output)