from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_consultancy import AddConsultancy
from use_cases.add_contractor import AddContractor


def test_can_add_contractor_to_consultancy():
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
        email="contractor@somewhere.com",
        start_date="2021-01-01"
    )

    verify_model(practice.contractors)


def test_can_add_multiple_contractors_to_consultancy():
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
        email="contractor@somewhere.com",
        start_date="2021-01-01"
    )
    AddContractor(practice).execute(
        code="2",
        name="Contractor 2",
        consultancy_code="1",
        email="contractor@somewhere.com",
        start_date="2021-01-01"
    )

    verify_model(practice.contractors)
