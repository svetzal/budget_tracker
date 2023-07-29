import pandas as pd
from tabulate import tabulate

from entities import Invoice, LineItem, HoursLineItem
from presentation import Colours


def print_dataframe(df):
    headers = [Colours.BOLD + Colours.UNDERLINE + col + Colours.RESET for col in df.columns]
    print(tabulate(df, headers, tablefmt='plain', showindex=False))


def aggregate_amounts():
    # Convert date_array into a dataframe
    holidays = pd.to_datetime(
        ['2023-01-02', '2023-02-20', '2023-04-07', '2023-05-22', '2023-07-03', '2023-08-07', '2023-09-04', '2023-10-09',
         '2023-12-25', '2023-12-26', '2024-01-01', '2024-02-19', '2024-04-01', '2024-05-20', '2024-07-01', '2024-08-05',
         '2024-09-02', '2024-10-14', '2024-12-25', '2024-12-26'])

    start_date = pd.to_datetime('2023-05-29')
    end_date = pd.to_datetime('2023-06-30')

    df = pd.read_excel('SampleDataFrame.xlsx')

    print_dataframe(df)

    df['LineItem.StartDate'] = pd.to_datetime(df['LineItem.StartDate'])
    df['LineItem.EndDate'] = pd.to_datetime(df['LineItem.EndDate'])

    # Calculate the total number of weekdays (excluding holidays) for each line item
    df['TotalDays'] = df.apply(lambda row: len(pd.bdate_range(row['LineItem.StartDate'], row['LineItem.EndDate'], freq="C", holidays=holidays)), axis=1)
    # df['TotalDays'] = df.apply(lambda row: len(pd.bdate_range(row['LineItem.StartDate'], row['LineItem.EndDate'])),
    #                            axis=1)

    df['QueryStart'] = df['LineItem.StartDate'].apply(lambda x: max(x, start_date))
    df['QueryEnd'] = df['LineItem.EndDate'].apply(lambda x: min(x, end_date))
    # df['QueryDays'] = (df['QueryEnd'] - df['QueryStart']).dt.days + 1
    df['QueryDays'] = df.apply(lambda row: len(pd.bdate_range(row['QueryStart'], row['QueryEnd'], freq="C", holidays=holidays)), axis=1)
    # df['QueryDays'] = df.apply(lambda row: len(pd.bdate_range(row['QueryStart'], row['QueryEnd'])), axis=1)
    df['QueryDays'] = df['QueryDays'].apply(
        lambda x: max(x, 0))  # to handle cases where the line item is outside the query period

    df['DailyRate'] = df['LineItem.Amount'] / df['TotalDays']
    df['QueryAmount'] = df['DailyRate'] * df['QueryDays']

    print(df)

    df_grouped = df.groupby(['Consultancy.Name', 'Contractor.Code'])
    df_agged = df_grouped.agg({
        'LineItem.Hours': 'sum',
        'LineItem.Amount': 'sum',
        'QueryDays': 'sum',
        'QueryAmount': 'sum',
    })

    print_dataframe(df_agged)


def join_objects():
    invoices = [
        Invoice(
            number="INV-001",
            issue_date="2023-06-03",
            period_start="2023-05-01",
            period_end="2023-05-31",
            line_items=[
                HoursLineItem(
                    description="Contractor 1 - 1st May to 31st May",
                    hours=37.5 * 4,
                    amount=37.5 * 4 * 225,
                    taxable=True,
                    contractor_code="CON-001",
                ),
                HoursLineItem(
                    description="Contractor 2 - 1st May to 31st May",
                    hours=37.5 * 4,
                    amount=37.5 * 4 * 225,
                    taxable=True,
                    contractor_code="CON-002",
                ),
            ]
        ),
        Invoice(
            number="INV-002",
            issue_date="2023-05-03",
            period_start="2023-04-01",
            period_end="2023-04-30",
            line_items=[
                HoursLineItem(
                    description="Contractor 1 - 1st April to 30th April",
                    hours=37.5 * 4,
                    amount=37.5 * 4 * 225,
                    taxable=True,
                    contractor_code="CON-001",
                ),
                HoursLineItem(
                    description="Contractor 2 - 1st April to 30th April",
                    hours=37.5 * 4,
                    amount=37.5 * 4 * 225,
                    taxable=True,
                    contractor_code="CON-002",
                ),
            ]
        ),
    ]

    df = None
    for i in invoices:
        for li in i.line_items:
            invoice_dict = i.dict()
            invoice_dict.pop('line_items')
            line_dict = li.dict()
            if df is None:
                df = pd.DataFrame([invoice_dict | line_dict])
            else:
                df = pd.concat([df, pd.DataFrame([invoice_dict | line_dict])])
    print_dataframe(df)


aggregate_amounts()
