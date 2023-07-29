import pytest

from data_types import Money
from entities import CoachingPracticeFinance, Consultancy, Contractor, Employee, FundingSource, SupportArea
from use_cases.test_data_generators import consultancy_details_generator, contractor_details_generator, \
    FIRST_CONSULTANCY_ID, SECOND_CONSULTANCY_ID, employee_details_generator, funding_source_details_generator, \
    support_area_details_generator, FIRST_SUPPORT_AREA_CODE, FIRST_TRANSIT, FIRST_EMPLOYEE_ID, SECOND_CONTRACTOR_CODE, \
    FIRST_CONTRACTOR_CODE, FIRST_SUPPORT_AREA_NUMBER


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
    return contractor_details_generator(FIRST_CONTRACTOR_CODE, FIRST_CONSULTANCY_ID)


@pytest.fixture
def second_contractor_details():
    return contractor_details_generator(SECOND_CONTRACTOR_CODE, FIRST_CONSULTANCY_ID)


@pytest.fixture
def first_employee_details():
    return employee_details_generator(FIRST_EMPLOYEE_ID)


@pytest.fixture
def first_funding_source_details():
    return funding_source_details_generator(FIRST_TRANSIT)


@pytest.fixture
def first_support_area_details():
    return support_area_details_generator(FIRST_SUPPORT_AREA_CODE, FIRST_SUPPORT_AREA_NUMBER)


@pytest.fixture
def practice_with_consultancy(empty_practice: CoachingPracticeFinance,
                              first_consultancy_details: dict) -> CoachingPracticeFinance:
    empty_practice.consultancies.append(
        Consultancy(**first_consultancy_details)
    )
    return empty_practice


@pytest.fixture
def practice_with_consultancy_and_contractor(practice_with_consultancy: CoachingPracticeFinance,
                                             first_contractor_details: dict) -> CoachingPracticeFinance:
    practice_with_consultancy.contractors.append(Contractor(**first_contractor_details))
    return practice_with_consultancy


@pytest.fixture
def staffed_practice(empty_practice: CoachingPracticeFinance,
                     first_consultancy_details: dict,
                     first_contractor_details: dict,
                     first_employee_details: dict,
                     first_funding_source_details: dict,
                     first_support_area_details: dict) -> CoachingPracticeFinance:
    empty_practice.consultancies.append(Consultancy(**first_consultancy_details))
    empty_practice.contractors.append(Contractor(**first_contractor_details))
    empty_practice.employees.append(Employee(**first_employee_details))
    empty_practice.funding_sources.append(FundingSource(
        transit=first_funding_source_details['transit'],
        name=first_funding_source_details['name'],
        total=Money(root=first_funding_source_details['total']),  # Ugh, this is ugly
        start_date=first_funding_source_details['start_date'],
        end_date=first_funding_source_details['end_date']
    ))
    empty_practice.support_areas.append(SupportArea(**first_support_area_details))
    return empty_practice


@pytest.fixture
def practice_with_multiple_consultancies(empty_practice,
                                         first_consultancy_details: dict,
                                         second_consultancy_details: dict) -> CoachingPracticeFinance:
    empty_practice.consultancies.append(
        Consultancy(**first_consultancy_details)
    )
    empty_practice.consultancies.append(
        Consultancy(**second_consultancy_details)
    )
    return empty_practice
