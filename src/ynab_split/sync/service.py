import asyncio
import polars as pl

from ynab_split.ynab.client import APIClient
from ynab_split.ynab.service import (
    get_categories_in_groups,
    list_transactions_in_categories,
    Transaction,
)

from ynab_split.sheets.service import get_spreadsheet

from .config import SyncSettings, YNABAccountSettings


def __ynab_client(account_settings: YNABAccountSettings):
    return APIClient(account_settings.access_token)


async def __get_transactions(account_settings: YNABAccountSettings) -> pl.DataFrame:
    client = __ynab_client(account_settings)

    cats = [
        c
        async for c in get_categories_in_groups(
            client,
            budget_id=account_settings.budget_id,
            groups=account_settings.groups,
        )
    ]

    transactions: list[Transaction] = [
        t.model_dump()
        async for t in list_transactions_in_categories(
            client,
            budget_id=account_settings.budget_id,
            since_date=account_settings.since_date,
            categories=cats,
        )
    ]

    schema = pl.Schema(
        [
            ("id", pl.String),
            ("date", pl.String),
            ("amount", pl.Int64),
            ("payee_name", pl.String),
            ("category_id", pl.String),
            ("category_name", pl.String),
            ("memo", pl.String),
            ("approved", pl.Boolean),
        ]
    )

    df = pl.from_dicts(transactions, schema=schema)
    df = df.with_columns(
        [
            pl.lit(account_settings.budget_id).alias("budget_id"),
            pl.lit(account_settings.name).alias("account_name"),
            (pl.col("amount").cast(pl.Float64) / 1000).round(2),
        ]
    )
    df = df.fill_null("")

    return df


async def get_all_transactions(settings: SyncSettings):
    tasks = [__get_transactions(s) for s in settings.accounts]
    dfs = await asyncio.gather(*tasks)

    all_transactions = pl.concat(dfs)

    return all_transactions


async def sync(settings: SyncSettings):
    all_transactions = await get_all_transactions(settings)

    # Add a column for each account
    for account in settings.accounts:
        all_transactions = all_transactions.with_columns(
            pl.lit(100.0).cast(pl.Float64).round(2).alias(f"{account.name} split")
        )

    spreadsheet = get_spreadsheet("Household Shared Transactions")
    sheet = spreadsheet.sheet1

    header = all_transactions.columns
    data = all_transactions.to_numpy().tolist()

    sheet.clear()
    return sheet.update([header] + data)
