import pandas as pd

from presentation import DataFrameRenderer
from use_cases.use_case import UseCase


class ListAreas(UseCase):
    def execute(self):
        areas = []
        for c in self.practice.contractors:
            for a in self.practice.support_areas:
                for s in self.practice.area_assignments:
                    if c.code == s.person_code and s.support_area_code == a.code:
                        areas.append([a.name, c.name, s.funding_source_transit, s.start_date, s.end_date])
        df = pd.DataFrame(areas, columns=["Area", "Contractor", "Funding Source", "Start Date", "End Date"])
        output = DataFrameRenderer(title="Area Assignments", data=df, sort_by=["Area", "Contractor"])
        return output.lines()
