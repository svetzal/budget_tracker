import pandas as pd

from presentation import DataFrameRenderer
from use_cases.use_case import UseCase


class ListConsultancies(UseCase):
    def execute(self):
        consultancies = []
        for o in self.practice.consultancies:
            for c in self.practice.contractors:
                if o.code == c.consultancy_code:
                    consultancies.append([o.code, o.name, c.code])
        df = pd.DataFrame(consultancies, columns=["Code", "Name", "Contractors"])
        aggregated = df.groupby(["Code", "Name"], as_index=False).count()
        output = DataFrameRenderer(title="Consultancies", data=aggregated, sort_by=["Name"])
        return output.lines()
