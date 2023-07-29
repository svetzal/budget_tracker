from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_consultancy import AddConsultancy
from use_cases.add_contractor import AddContractor
from use_cases.add_transaction_agreement import AddTransactionAgreement
from use_cases.test_data_generators import FIRST_CONTRACTOR_CODE


def test_add_transaction_agreement(practice_with_consultancy_and_contractor: CoachingPracticeFinance):
    AddTransactionAgreement(practice_with_consultancy_and_contractor).execute(
        number="1",
        contractor_code=FIRST_CONTRACTOR_CODE,
        hours=10,
        rate=100.00,
        start_date="2021-01-01",
        end_date="2021-12-31"
    )

    verify_model(practice_with_consultancy_and_contractor.transaction_agreements)
