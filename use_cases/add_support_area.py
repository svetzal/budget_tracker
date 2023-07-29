from entities import SupportArea
from use_cases.use_case import UseCase


class AddSupportArea(UseCase):
    def execute(self, **kwargs):
        support_area = SupportArea(**kwargs)
        if support_area not in self.practice.support_areas:
            self.practice.support_areas.append(support_area)
