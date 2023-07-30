from entities import CoachingPracticeFinance
from use_cases.list_transaction_agreements_by_contractor import ListTransactionAgreementsByContractor
from verifiers import verify_report


def test_can_list_transaction_agreements(staffed_practice: CoachingPracticeFinance):
    output = ListTransactionAgreementsByContractor(staffed_practice).execute()

    verify_report(output)