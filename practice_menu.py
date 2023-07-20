import inspect

from entities import CoachingPracticeFinance
from presentation import Colours
from report_use_cases import ListPeople, ListConsultancies, CurrentFiscalYearMonthly, NextFiscalYearBudgetMonthly
from use_cases import AddConsultancy, AddContractor, AddEmployee, AddTransactionAgreement


def main():
    practice = CoachingPracticeFinance.load()

    functions = {
        'add_consultancy': {
            'func': AddConsultancy(practice).execute,
            'label': 'Add Consultancy'
        },
        'list_consultancies': {
            'func': ListConsultancies(practice).execute,
            'label': 'List Consultancies'
        },
        'add_contractor': {
            'func': AddContractor(practice).execute,
            'label': 'Add Contractor'
        },
        'add_employee': {
            'func': AddEmployee(practice).execute,
            'label': 'Add Employee'
        },
        'list_people': {
            'func': ListPeople(practice).execute,
            'label': 'List People'
        },
        'add_transaction_agreement': {
            'func': AddTransactionAgreement(practice).execute,
            'label': 'Add Transaction Agreement'
        },
        'current_fiscal_year_monthly': {
            'func': CurrentFiscalYearMonthly(practice).execute,
            'label': 'Current Fiscal Year Monthly'
        },
        'next_fiscal_year_budget_monthly': {
            'func': NextFiscalYearBudgetMonthly(practice).execute,
            'label': 'Next Fiscal Year Budget Monthly'
        }
    }

    while True:
        print("")
        print(Colours.HEADER + Colours.UNDERLINE + "Digital Agile Coaching Practice" + Colours.RESET)
        print("")
        print("Menu:")
        print(f"{Colours.OKGREEN}-1{Colours.RESET} - Exit Without Saving")
        print(f" {Colours.OKGREEN}0{Colours.RESET} - Save & Exit")
        for i, key in enumerate(functions.keys()):
            print(f" {Colours.OKGREEN}{i + 1}{Colours.RESET} - {functions[key]['label']}")
        print("")

        choice = int(input("Enter choice: "))

        if choice == -1:
            exit()

        if choice == 0:
            practice.save()
            exit()

        chosen_func = list(functions.values())[choice - 1]['func']
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
