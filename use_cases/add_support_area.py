from entities import SupportArea
from use_cases.use_case import UseCase


class AddSupportArea(UseCase):
    def execute(self, code: str, name: str):
        self.guard_support_area_not_duplicate(code)
        support_area = SupportArea(code=code, name=name)
        self.practice.support_areas.append(support_area)
