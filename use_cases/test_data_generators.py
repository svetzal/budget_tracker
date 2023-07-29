FIRST_CONSULTANCY_ID = 1
SECOND_CONSULTANCY_ID = 2

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


def funding_source_details_generator(transit):
    return {
        "transit": transit,
        "name": f"Bank {transit}",
        "total": 1000,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
    }


def support_area_details_generator(id):
    return {
        "code": f"area{id}",
        "name": f"Area {id}",
    }
