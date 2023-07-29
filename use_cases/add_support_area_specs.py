from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_support_area import AddSupportArea


def test_can_add_support_area(empty_practice, first_support_area_details: dict):
    AddSupportArea(empty_practice).execute(**first_support_area_details)

    verify_model(empty_practice.support_areas)