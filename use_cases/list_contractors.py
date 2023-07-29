from datetime import date

import pandas as pd

from presentation import DataFrameRenderer
from use_cases.use_case import UseCase


class ListContractors(UseCase):
    def execute(self):
        contractors = []
        for consultancy in self.practice.consultancies:
            for c in self.practice.contractors:
                if c.consultancy_code == consultancy.code:
                    ta_found = False
                    for ta in self.practice.transaction_agreements:
                        if ta.contractor_code == c.code:
                            if ta.start_date <= date.today() <= ta.end_date:
                                ta_found = True
                                contractors.append(
                                    [c.code, c.name, consultancy.name, ta.number, ta.rate, ta.hours, ta.start_date,
                                     ta.end_date])
                    if not ta_found:
                        contractors.append([c.code, c.name, consultancy.name, None, None, "", None, None])
        df = pd.DataFrame(contractors,
                          columns=["Code", "Name", "Consultancy", "Agreement", "Rate", "Hours", "Start", "End"])
        output = DataFrameRenderer(title="Contractors", data=df, sort_by=["Name"])
        return output.lines()
