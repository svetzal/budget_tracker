import argparse

from use_cases import AddConsultancy
from entities import Consultancy, CoachingPracticeFinance


def main(args):
    practice = CoachingPracticeFinance.parse_file("practice.json")

    add_consultancy = AddConsultancy(practice)
    add_consultancy.execute(
        Consultancy(
            code=args.code,
            name=args.name,
            contract=args.contract,
            contact_name=args.contact_name,
            contact_phone=args.contact_phone,
            contact_email=args.contact_email
        )
    )

    with open("practice.json", "w") as f:
        f.write(practice.json(indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="add_vendor.py",
        description="A system to manage practice finances",
        epilog="If you need help, ask Stacey",
    )

    parser.add_argument('code')
    parser.add_argument('name')
    parser.add_argument('contract')
    parser.add_argument('contact_name')
    parser.add_argument('contact_phone')
    parser.add_argument('contact_email')

    args = parser.parse_args()

    main(args)
