from datetime import date

from entities import AreaAssignment
from use_cases.use_case import UseCase


class AddAreaAssignment(UseCase):
    def execute(self, support_area_code: str, person_code: str, funding_source_transit: int, start_date: str, end_date: str):
        self.guard_support_area_exists(support_area_code)
        self.guard_contractor_exists(person_code)
        self.guard_funding_source_exists(funding_source_transit)
        area_assignment = AreaAssignment(
            support_area_code=support_area_code,
            person_code=person_code,
            funding_source_transit=funding_source_transit,
            start_date=date.fromisoformat(start_date),
            end_date=date.fromisoformat(end_date)
        )
        self.practice.area_assignments.append(area_assignment)
