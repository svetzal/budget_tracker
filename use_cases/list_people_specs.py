from entities import CoachingPracticeFinance
from use_cases.list_people import ListPeople
from verifiers import verify_report


def test_can_list_people(staffed_practice: CoachingPracticeFinance):
    output = ListPeople(staffed_practice).execute()

    verify_report(output)