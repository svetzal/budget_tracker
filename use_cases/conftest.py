import pytest
from entities import CoachingPracticeFinance, Consultancy
from use_cases.test_data_generators import consultancy_details_generator, contractor_details_generator, \
    FIRST_CONSULTANCY_ID, SECOND_CONSULTANCY_ID, employee_details_generator


@pytest.fixture
def empty_practice() -> CoachingPracticeFinance:
    return CoachingPracticeFinance()


@pytest.fixture
def first_consultancy_details():
    return consultancy_details_generator(FIRST_CONSULTANCY_ID)


@pytest.fixture
def second_consultancy_details():
    return consultancy_details_generator(SECOND_CONSULTANCY_ID)


@pytest.fixture
def first_contractor_details():
    return contractor_details_generator(1, FIRST_CONSULTANCY_ID)


@pytest.fixture
def second_contractor_details():
    return contractor_details_generator(2, FIRST_CONSULTANCY_ID)


@pytest.fixture
def first_employee_details():
    return employee_details_generator(1)


@pytest.fixture
def practice_with_consultancy(empty_practice: CoachingPracticeFinance,
                              first_consultancy_details: dict) -> CoachingPracticeFinance:
    empty_practice.consultancies.append(
        Consultancy(**first_consultancy_details)
    )
    return empty_practice


@pytest.fixture
def practice_with_multiple_consultancies(empty_practice: CoachingPracticeFinance,
                                         first_consultancy_details: dict,
                                         second_consultancy_details: dict) -> CoachingPracticeFinance:
    empty_practice.consultancies.append(
        Consultancy(**first_consultancy_details)
    )
    empty_practice.consultancies.append(
        Consultancy(**second_consultancy_details)
    )
    return empty_practice
