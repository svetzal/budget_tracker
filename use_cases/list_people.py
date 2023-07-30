import pandas as pd

from presentation import DataFrameRenderer
from use_cases.use_case import UseCase


class ListPeople(UseCase):
    def execute(self):
        people = []
        for c in self.practice.consultancies:
            for p in self.practice.contractors:
                if c.code == p.consultancy_code:
                    people.append([p.code, p.name, c.name, p.start_date, p.end_date])
        for p in self.practice.employees:
            people.append([p.code, p.name, "Coaching Practice", p.start_date, p.end_date])
        df = pd.DataFrame(people, columns=["Code", "Name", "Company", "Start Date", "End Date"])
        output = DataFrameRenderer(title="People", data=df, sort_by=["Name"])
        return output.lines()
