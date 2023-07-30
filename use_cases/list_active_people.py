import pandas as pd

from presentation import DataFrameRenderer
from use_cases.list_people import ListPeople


class ListActivePeople(ListPeople):
    def execute(self):
        people = []
        for c in self.practice.consultancies:
            for p in self.practice.contractors:
                if c.code == p.consultancy_code and p.end_date is None:
                    people.append([p.code, p.name, c.name])
        for p in self.practice.employees:
            if p.end_date is None:
                people.append([p.code, p.name, "Coaching Practice"])
        df = pd.DataFrame(people, columns=["Code", "Name", "Company"])
        output = DataFrameRenderer(title="Active People", data=df, sort_by=["Name"])
        return output.lines()