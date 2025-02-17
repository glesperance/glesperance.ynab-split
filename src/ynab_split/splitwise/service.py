from splitwise import Splitwise
from splitwise.group import Group
from splitwise.debt import Debt
from splitwise.expense import Expense, ExpenseUser
from ynab_split.splitwise.config import splitwise_client_settings

from datetime import date, datetime
import polars as pl

def describe_groups(client: Splitwise):
    groups: list[Group] = client.getGroups()


    for g in groups:
        print("Group: ", g.name)
        print("Group ID: ", g.id)
        print("Group Created At: ", g.created_at)
        print("Group Updated At: ", g.updated_at)
        for _sd in g.getSimplifiedDebts():
            sd: Debt = _sd
            print(f"  ({sd.fromUser}) owes ({sd.toUser}) {sd.amount}")
        print("Group Members: ")
        for m in g.members:
            print(f"  ({m.id}) {m.first_name} {m.last_name} ({m.email})")
        print("-" * 100)

def get_group_expenses(client: Splitwise, *, group_id: int, visible_only: bool = True) -> pl.DataFrame:
    expenses = client.getExpenses(group_id=group_id, visible=visible_only)
    schema = pl.Schema(
        [
            ("id", pl.Int64),
            ("group_id", pl.Int64),
            ("cost", pl.Float64),
            ("date", pl.Date),
            ("description", pl.String),
            ("details", pl.String),
        ]
    )
    return pl.from_dicts(
        [
            {
                "id": e.id,
                "group_id": e.group_id,
                "cost": e.cost,
                "date": datetime.fromisoformat(e.date).date(),
                "description": e.description,
                "details": e.details,
            }
            for e in expenses
        ],
        schema=schema
    )

def create_group_expense(
        client: Splitwise,
        *,
        group_id: int,
        amount: float,
        date: date, 
        description: str,
        details: str
    ):

    # Get the current user 
    current_user = client.getCurrentUser()
    assert current_user is not None, "Current user is not set"
    members = client.getGroup(group_id).getMembers()
    
    assert current_user.id in [m.id for m in members], "Current user is not in the group"
    other_members = [m for m in members if m.id != current_user.id]

    assert len(members) > 0, "Group has no members"
    # Assert current user is in the group

    exp = Expense()
    exp.setGroupId(group_id)
    exp.setDescription(description)
    exp.setCost(amount)
    exp.setDate(date.strftime("%Y-%m-%d"))
    exp.setDetails(details)

    # Calculate rounded share per person
    share_per_person = round(amount / (len(other_members) + 1), 2)
    
    # Calculate total of rounded shares for all members except current user
    total_others_shares = share_per_person * len(other_members)
    
    # Current user's share is the remainder to ensure total equals amount exactly
    current_user_share = round(amount - total_others_shares, 2)

    # Current user is the one who pays, expense is split evenly
    u0 = ExpenseUser()
    u0.setId(current_user.id)
    u0.setPaidShare(amount)
    u0.setOwedShare(current_user_share)

    expense_users = [u0]
    for m in other_members:
        u = ExpenseUser()
        u.setId(m.id)
        u.setPaidShare(0)
        u.setOwedShare(share_per_person)
        expense_users.append(u)

    exp.setUsers(expense_users)

    exp, err = client.createExpense(exp)

    assert err is None, f"Error creating expense: {err.__dict__}"
    return exp