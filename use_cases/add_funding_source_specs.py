from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_funding_source import AddFundingSource


def test_can_add_funding_source(empty_practice: CoachingPracticeFinance, first_funding_source_details: dict):
    AddFundingSource(empty_practice).execute(**first_funding_source_details)

    verify_model(empty_practice.funding_sources)