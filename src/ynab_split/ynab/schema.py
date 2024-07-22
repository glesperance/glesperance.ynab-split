from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id: str
    name: str
    hidden: bool


class CategoryGroup(BaseModel):
    id: str
    name: str
    categories: list[Category]


class Transaction(BaseModel):
    id: str
    date: str
    amount: int
    payee_name: str | None
    category_id: str
    category_name: str
    memo: str | None
    approved: bool


CategoryId = str
CategoryGroupName = str
