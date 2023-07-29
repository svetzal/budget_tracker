from entities import CoachingPracticeFinance
from use_cases.report_next_fiscal_year_monthly import NextFiscalYearBudgetMonthly
from verifiers import verify_report


def test_can_report_next_fiscal_monthly_budget(staffed_practice: CoachingPracticeFinance):

    output = NextFiscalYearBudgetMonthly(staffed_practice).execute()

    verify_report(output)
