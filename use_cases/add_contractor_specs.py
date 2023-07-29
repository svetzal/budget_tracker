from entities import CoachingPracticeFinance
from verifiers import verify_model
from use_cases.add_contractor import AddContractor
from use_cases.test_data_generators import contractor_details_generator, FIRST_CONSULTANCY_ID


def test_can_add_contractor_to_consultancy(practice_with_consultancy: CoachingPracticeFinance,
                                           first_contractor_details: dict):
    AddContractor(practice_with_consultancy).execute(**first_contractor_details)

    verify_model(practice_with_consultancy.contractors)


def test_can_add_multiple_contractors_to_consultancy(practice_with_consultancy: CoachingPracticeFinance):
    first_contractor_details = contractor_details_generator(1, FIRST_CONSULTANCY_ID)
    second_contractor_details = contractor_details_generator(2, FIRST_CONSULTANCY_ID)

    AddContractor(practice_with_consultancy).execute(**first_contractor_details)
    AddContractor(practice_with_consultancy).execute(**second_contractor_details)

    verify_model(practice_with_consultancy.contractors)


def test_cant_add_contractor_to_nonexistent_consultancy(empty_practice,
                                                        first_contractor_details: dict):
    try:
        AddContractor(empty_practice).execute(**first_contractor_details)
        assert False, "Should have failed with ValueError"
    except ValueError:
        pass
    verify_model(empty_practice.contractors)


def test_cant_add_duplicate_contractor(practice_with_consultancy: CoachingPracticeFinance,
                                       first_contractor_details: dict):
    AddContractor(practice_with_consultancy).execute(**first_contractor_details)
    try:
        AddContractor(practice_with_consultancy).execute(**first_contractor_details)
        assert False, "Should have failed with ValueError"
    except ValueError:
        pass
    verify_model(practice_with_consultancy.contractors)
