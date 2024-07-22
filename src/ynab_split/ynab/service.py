from datetime import date
from .schema import (
    CategoryId,
    CategoryGroupName,
    Category,
    CategoryGroup,
    Transaction,
)
from .client import APIClient


async def get_categories_in_groups(
    client: APIClient,
    *,
    budget_id: str,
    groups: list[CategoryGroupName] | CategoryGroupName,
    ignore_hidden: bool = True,
) -> list[CategoryId]:
    res = await client.get(f"/budgets/{budget_id}/categories")

    for _cg in res["data"]["category_groups"]:
        cg = CategoryGroup.model_validate(_cg)
        if cg.name in groups:
            for c in cg.categories:
                if ignore_hidden and c.hidden:
                    continue
                yield c


async def list_transactions_in_categories(
    client: APIClient,
    *,
    budget_id: str,
    categories: list[Category] | Category | CategoryId | list[CategoryId],
    since_date: date,
    approved_only: bool = True,
):

    if not isinstance(categories, list):
        categories = [categories]

    category_ids = (
        [c.id for c in categories]
        if isinstance(categories[0], Category)
        else categories
    )

    for c_id in category_ids:
        res = await client.get(
            f"/budgets/{budget_id}/categories/{c_id}/transactions",
            {"since_date": since_date.isoformat()},
        )

        assert isinstance(res["data"]["transactions"], list)
        for _t in res["data"]["transactions"]:
            t = Transaction.model_validate(_t)
            if approved_only and not t.approved:
                continue
            yield t
