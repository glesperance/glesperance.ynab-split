from pydantic import BaseModel
from datetime import date
from ynab_split.ynab.config import CategoryGroupName


class YNABAccountSettings(BaseModel):
    name: str
    access_token: str
    budget_id: str
    since_date: date
    groups: list[CategoryGroupName]


class SyncSettings(BaseModel):
    accounts: list[YNABAccountSettings]
