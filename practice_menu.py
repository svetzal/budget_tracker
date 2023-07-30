import inspect
from typing import List

from entities import CoachingPracticeFinance
from presentation import Colours
from use_cases.add_area_assignment import AddAreaAssignment
from use_cases.list_active_people import ListActivePeople
from use_cases.list_transaction_agreements_by_contractor import ListTransactionAgreementsByContractor
from use_cases.report_next_fiscal_year_monthly import NextFiscalYearBudgetMonthly
from use_cases.report_current_fiscal_year_monthly import CurrentFiscalYearMonthly
from use_cases.list_consultancies import ListConsultancies
from use_cases.list_people import ListPeople
from use_cases.add_transaction_agreement import AddTransactionAgreement
from use_cases.add_employee import AddEmployee
from use_cases.add_contractor import AddContractor
from use_cases.add_consultancy import AddConsultancy


def main():
    practice = CoachingPracticeFinance.load()

    functions: List[dict] = [
        {
            'func': AddAreaAssignment(practice).execute,
            'label': 'Add Area Assignment'
        },
        {
            'func': AddConsultancy(practice).execute,
            'label': 'Add Consultancy'
        },
        {
            'func': ListConsultancies(practice).execute,
            'label': 'List Consultancies'
        },
        {
            'func': AddContractor(practice).execute,
            'label': 'Add Contractor'
        },
        {
            'func': AddEmployee(practice).execute,
            'label': 'Add Employee'
        },
        {
            'func': ListPeople(practice).execute,
            'label': 'List People'
        },
        {
            'func': ListActivePeople(practice).execute,
            'label': 'List Active People'
        },
        {
            'func': AddTransactionAgreement(practice).execute,
            'label': 'Add Transaction Agreement'
        },
        {
            'func': ListTransactionAgreementsByContractor(practice).execute,
            'label': 'List Transaction Agreements By Contractor'
        },
        {
            'func': CurrentFiscalYearMonthly(practice).execute,
            'label': 'Current Fiscal Year Monthly'
        },
        {
            'func': NextFiscalYearBudgetMonthly(practice).execute,
            'label': 'Next Fiscal Year Budget Monthly'
        },
    ]

    while True:
        print("")
        print(Colours.HEADER + Colours.UNDERLINE + "Digital Agile Coaching Practice" + Colours.RESET)
        print("")
        print("Menu:")
        print(f"{Colours.OKGREEN}-1{Colours.RESET} - Exit Without Saving")
        print(f" {Colours.OKGREEN}0{Colours.RESET} - Save & Exit")
        for i, function in enumerate(functions):
            print(f" {Colours.OKGREEN}{i + 1}{Colours.RESET} - {function['label']}")
        print("")

        choice = int(input("Enter choice: "))

        if choice == -1:
            exit()

        if choice == 0:
            practice.save()
            exit()

        chosen_func = functions[choice-1]['func']
        argspec = inspect.getfullargspec(chosen_func)
        args = {}
        for i, arg in enumerate(argspec.args):
            if arg == 'self':
                continue
            if argspec.defaults:
                default = argspec.defaults[i]
                value = input(
                    f"Enter {Colours.BOLD}{arg}{Colours.RESET} (default is {Colours.OKGREEN}{default}{Colours.RESET}): ")
                args[arg] = value if value else default
            else:
                args[arg] = input(f"Enter {arg}: ")

        result = chosen_func(**args)

        if result:
            print("\n".join(result))


if __name__ == "__main__":
    main()
