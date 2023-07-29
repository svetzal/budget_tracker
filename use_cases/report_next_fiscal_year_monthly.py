from datetime import date

import pandas as pd
from dateutil.relativedelta import relativedelta

from use_cases.use_case import UseCase


class NextFiscalYearBudgetMonthly(UseCase):

    def execute(self):
        data = []
        return data