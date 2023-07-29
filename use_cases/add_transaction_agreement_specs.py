from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_consultancy import AddConsultancy
from use_cases.add_contractor import AddContractor
from use_cases.add_transaction_agreement import AddTransactionAgreement


def test_add_transaction_agreement():
    practice = CoachingPracticeFinance()

    AddConsultancy(practice).execute(
        code="1",
        name="Consultancy 1",
        contract="CTR00123",
        contact_name="Someone",
        contact_phone="647-555-1212",
        contact_email="someone@somewhere.com"
    )

    AddContractor(practice).execute(
        code="1",
        name="Contractor 1",
        consultancy_code="1",
        email="someone@somewhere.com",
        start_date="2021-01-01"
    )

    AddTransactionAgreement(practice).execute(
        number="1",
        contractor_code="1",
        hours=10,
        rate=100.00,
        start_date="2021-01-01",
        end_date="2021-12-31"
    )

    verify_model(practice.transaction_agreements)
