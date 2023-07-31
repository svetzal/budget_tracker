from datetime import date
from typing import Optional

from entities import AreaAssignment, LEVEL_PROGRAM, LEVEL_EXECUTIVE
from use_cases.use_case import UseCase


class AddAreaAssignment(UseCase):
    def execute(self, support_area_code: str, person_code: str, funding_source_transit: int, start_date: str,
                end_date: str, level: Optional[str]):
        self.guard_support_area_must_exist(support_area_code)
        self.guard_person_must_exist(person_code)
        self.guard_funding_source_must_exist(funding_source_transit)
        if level not in [LEVEL_EXECUTIVE, LEVEL_PROGRAM]:
            raise ValueError(f"Level must be 'exec' or 'program', not {level}")
        area_assignment = AreaAssignment(
            support_area_code=support_area_code,
            person_code=person_code,
            funding_source_transit=funding_source_transit,
            level=level,
            start_date=date.fromisoformat(start_date),
            end_date=date.fromisoformat(end_date)
        )
        self.practice.area_assignments.append(area_assignment)
