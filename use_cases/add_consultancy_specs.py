from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_consultancy import AddConsultancy


def test_can_add_consultancy():
    practice = CoachingPracticeFinance()
    AddConsultancy(practice).execute(
        code="1",
        name="Consultancy 1",
        contract="CTR00123",
        contact_name="Someone",
        contact_phone="647-555-1212",
        contact_email="someone@somewhere.com"
    )
    verify_model(practice.consultancies)
