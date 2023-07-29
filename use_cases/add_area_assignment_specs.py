from _decimal import Decimal

from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_area_assignment import AddAreaAssignment
from use_cases.add_consultancy import AddConsultancy
from use_cases.add_contractor import AddContractor
from use_cases.add_funding_source import AddFundingSource
from use_cases.add_support_area import AddSupportArea


def test_add_area_assignment():
    practice = CoachingPracticeFinance()

    AddSupportArea(practice).execute(
        code="1",
        name="Area 1"
    )

    AddFundingSource(practice).execute(
        transit=1,
        name="Funding Source 1",
        total=Decimal(100000),
        start_date="2020-01-01",
        end_date="2020-12-31",
    )

    AddConsultancy(practice).execute(
        code="1",
        name="Consultancy 1",
        contract="CTR00123",
        contact_name="Someone",
        contact_phone="647-555-1212",
        contact_email="someone@somewhere.com",
    )

    AddContractor(practice).execute(
        code="1",
        name="Contractor 1",
        consultancy_code="1",
        phone_number="647-555-1212",
        email="someone@somewhere.com",
        start_date="2020-01-01",
    )

    AddAreaAssignment(practice).execute(
        support_area_code="1",
        contractor_code="1",
        funding_source_transit=1,
        start_date="2020-01-01",
        end_date="2020-12-31",
    )

    verify_model(practice.area_assignments)