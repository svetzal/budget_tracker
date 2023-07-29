from _decimal import Decimal

from data_types import Money

FIRST_CONSULTANCY_ID = "1"
SECOND_CONSULTANCY_ID = "2"
FIRST_SUPPORT_AREA_NUMBER = 1
FIRST_SUPPORT_AREA_CODE = "area1"
FIRST_TRANSIT = 1
FIRST_CONTRACTOR_CODE = "1"
SECOND_CONTRACTOR_CODE = "2"
FIRST_EMPLOYEE_ID = "1"


def consultancy_details_generator(id: int):
    return {
        "code": str(id),
        "name": f"Consultancy {id}",
        "contract": f"CTR00{id}",
        "contact_name": "Someone",
        "contact_phone": "647-555-1212",
        "contact_email": f"someone@consultancy{id}.com",
    }


def contractor_details_generator(id: int, consultancy: int):
    return {
        "code": str(id),
        "name": f"Contractor {id}",
        "consultancy_code": str(consultancy),
        "email": f"contractor{id}@consultancy{consultancy}.com",
        "start_date": "2023-01-01",
    }


def employee_details_generator(id):
    return {
        "code": str(id),
        "name": f"Employee {id}",
        "email": f"employee{id}.name@mycompany.com",
        "start_date": "2021-01-01"
    }


def funding_source_details_generator(transit: int):
    return {
        "transit": transit,
        "name": f"Bank {transit}",
        "total": Decimal(1000),
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
    }


def support_area_details_generator(id: str, number: int = 1):
    return {
        "code": id,
        "name": f"Area {number}",
    }
