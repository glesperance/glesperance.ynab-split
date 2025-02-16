from pydantic import BaseModel
from datetime import date
from typing import Optional
from ynab_split.ynab.config import CategoryGroupName


class YNABAccountSettings(BaseModel):
    name: str
    ynab_access_token: str
    ynab_budget_id: str
    since_date: date
    groups: list[CategoryGroupName]
    splitwise_group_id: Optional[int] = None


class SyncSettings(BaseModel):
    accounts: list[YNABAccountSettings]
