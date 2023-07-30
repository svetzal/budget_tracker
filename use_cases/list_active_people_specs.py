from entities import CoachingPracticeFinance
from use_cases.list_active_people import ListActivePeople
from verifiers import verify_report


def test_can_list_people(staffed_practice: CoachingPracticeFinance):
    output = ListActivePeople(staffed_practice).execute()

    verify_report(output)