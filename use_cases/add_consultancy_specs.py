from entities import CoachingPracticeFinance
from model_verifier import verify_model
from use_cases.add_consultancy import AddConsultancy


def test_can_add_consultancy(empty_practice, first_consultancy_details: dict):
    AddConsultancy(empty_practice).execute(**first_consultancy_details)
    verify_model(empty_practice.consultancies)


def test_can_add_multiple_consultancies(empty_practice, first_consultancy_details: dict,
                                        second_consultancy_details: dict):
    AddConsultancy(empty_practice).execute(**first_consultancy_details)
    AddConsultancy(empty_practice).execute(**second_consultancy_details)
    verify_model(empty_practice.consultancies)


def test_fails_when_adding_duplicate_consultancy(empty_practice,
                                                 first_consultancy_details: dict):
    AddConsultancy(empty_practice).execute(**first_consultancy_details)
    try:
        AddConsultancy(empty_practice).execute(**first_consultancy_details)
        assert False, "Should have failed with ValueError"
    except ValueError:
        pass
    verify_model(empty_practice.consultancies)
