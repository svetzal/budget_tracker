from entities import CoachingPracticeFinance
from use_cases.list_contractors import ListContractors
from verifiers import verify_report


def test_can_list_contractors(staffed_practice: CoachingPracticeFinance):
    output = ListContractors(staffed_practice).execute()

    verify_report(output)