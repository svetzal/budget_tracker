from entities import CoachingPracticeFinance
from use_cases.list_consultancies import ListConsultancies
from verifiers import verify_report


def test_can_list_consultancies(staffed_practice: CoachingPracticeFinance):
    output = ListConsultancies(staffed_practice).execute()

    verify_report(output)