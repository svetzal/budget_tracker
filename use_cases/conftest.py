from _decimal import Decimal

import pytest

from data_types import Money
from entities import CoachingPracticeFinance, Consultancy, Contractor, Employee, FundingSource, SupportArea, \
    AreaAssignment, TransactionAgreement
from use_cases.test_data_generators import consultancy_details_generator, contractor_details_generator, \
    FIRST_CONSULTANCY_CODE, SECOND_CONSULTANCY_ID, employee_details_generator, funding_source_details_generator, \
    support_area_details_generator, FIRST_SUPPORT_AREA_CODE, FIRST_TRANSIT, FIRST_EMPLOYEE_CODE, SECOND_CONTRACTOR_CODE, \
    FIRST_CONTRACTOR_CODE, FIRST_SUPPORT_AREA_NUMBER, FIRST_INVOICE_NUMBER


@pytest.fixture
def empty_practice() -> CoachingPracticeFinance:
    return CoachingPracticeFinance()


@pytest.fixture
def first_consultancy_details():
    return consultancy_details_generator(FIRST_CONSULTANCY_CODE)


@pytest.fixture
def second_consultancy_details():
    return consultancy_details_generator(SECOND_CONSULTANCY_ID)


@pytest.fixture
def first_contractor_details():
    return contractor_details_generator(FIRST_CONTRACTOR_CODE, FIRST_CONSULTANCY_CODE)


@pytest.fixture
def second_contractor_details():
    return contractor_details_generator(SECOND_CONTRACTOR_CODE, FIRST_CONSULTANCY_CODE)


@pytest.fixture
def first_employee_details():
    return employee_details_generator(FIRST_EMPLOYEE_CODE)


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
    empty_practice.transaction_agreements.append(
        TransactionAgreement(
            number="1",
            contractor_code=FIRST_CONTRACTOR_CODE,
            hours=100,
            rate=Money.from_int(100),
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
    )
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
def operational_practice(staffed_practice: CoachingPracticeFinance):
    staffed_practice.area_assignments.append(
        AreaAssignment(
            support_area_code=FIRST_SUPPORT_AREA_CODE,
            person_code=FIRST_CONTRACTOR_CODE,
            funding_source_transit=FIRST_TRANSIT,
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
    )
    return staffed_practice


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


@pytest.fixture
def first_invoice_details():
    first_invoice_details = {
        "consultancy_code": FIRST_CONSULTANCY_CODE,
        "number": FIRST_INVOICE_NUMBER,
        "issue_date": "2023-01-07",
    }
    return first_invoice_details


@pytest.fixture
def first_hours_line_item_details():
    return {
        "invoice_number": FIRST_INVOICE_NUMBER,
        "description": "Hours for first week",
        "amount": Decimal(4000),
        "contractor_code": FIRST_CONTRACTOR_CODE,
        "taxable": True,
        "hours": 40,
        "period_start": "2023-01-01",
        "period_end": "2023-01-07",
    }


@pytest.fixture
def first_expense_details():
    first_expense_details = {
        "invoice_number": FIRST_INVOICE_NUMBER,
        "description": "Expenses for first week",
        "amount": Decimal(100),
        "contractor_code": FIRST_CONTRACTOR_CODE,
        "taxable": False,
    }
    return first_expense_details
