import json
from datetime import datetime, date
import calendar
import argparse

DATA_FILE = "data/expenses.json"

CATEGORIES = [
"Sustenance", "Housing", "Transportation",
"Bills", "Shopping", "Entertainment",
"Health & Fitness", "Education", "Savings & Investments",
"Debt Payments", "Gifts & Donations", "Travel", "Other"
]

def verify_category(category: str):
    category = category.strip().capitalize()
    if category in CATEGORIES:
        return category
    else:
        raise ValueError(f"Invalid category: {category}. Must be one of {CATEGORIES}.")

def load_expenses():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)
#retro function
def input_detail():

    print("Select a category:")
    while True:
        for i, cat in enumerate(CATEGORIES, start=1):
            print(f"{i}. {cat}")
        choice = input("Enter number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            category = CATEGORIES[int(choice)-1]
            break
        print("Invalid input. Try again.")
    
    desc = input("Enter description: ")
    while True:
        amount = input("Enter amount: ")
        if amount.lower() == "exit":
            return None
        try:
            float(amount)
            break
        except ValueError:
            print("Invalid amount. Try again.")

    while True:
        date = input("Enter date (YYYY-MM-DD/today/exit): ")
        if date == "exit":
            return None
        if date.lower() == "today":
            date = datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Try again.")

    return {
        "date": date,
        "category": category,
        "desc": desc,
        "amount": amount
    }

#list mutation functions
def add_expense(date, category, desc, amount):

    expenses = load_expenses()
    next_id = (max([e["id"] for e in expenses]) + 1) if expenses else 1
    # user_input = input_detail()

    # if user_input is None:
    #     print("Action cancelled.")
    #     return  

    expenses.append({
        "id": next_id,
        "date": date,
        "category": category,
        "desc": desc,
        "amount": amount
    })

    save_expenses(expenses)
    print("Expense added!")

def edit_expense(id, date=None, category=None, desc=None, amount=None):
    expenses = load_expenses()
    for exp in expenses:
        if exp["id"] == id:
            new_data = {} 
            if date:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    new_data["date"] = date
                except ValueError:
                    print("Invalid date, format: YYYY-MM-DD")
            if category:
                new_data["category"] = category
            if desc:
                new_data["desc"] = desc
            if amount:
                new_data["amount"] = amount

            exp.update(new_data)
            save_expenses(expenses)
            print(f"Expense {id} updated!")
            return

    print(f"No expense found with ID {id}")


def delete_expense(expense_id):
    expenses = load_expenses()
    # while True:
    #     expense_id = input("id: ")

    #     if expense_id.lower() == "exit":
    #         return

    new_expenses = [exp for exp in expenses if exp.get("id") != int(expense_id)]

    if len(expenses) == len(new_expenses):
        print(f"No expense found with ID {expense_id}")
        return

    save_expenses(new_expenses)
    print(f"Expense {expense_id} deleted!")

#listing
def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return
    for exp in expenses:
        print(f"{exp['id']}. {exp['date']} | {exp['category']} | {exp['desc']} | {exp['amount']}")

#filters
def filter_by_category(category):
    expenses = load_expenses()
    # while True:
    #     for i, cat in enumerate(CATEGORIES, start=1):
    #         print(f"{i}. {cat}")
    #     choice = input("Enter number: ")
    #     if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
    #         category = CATEGORIES[int(choice)-1]
    #         break
    #     print("Invalid input. Try again.")
    [print(exp) for exp in expenses if exp.get("category") == category]

def filter_by_date(start_str, end_str):
    expenses = load_expenses()
    while True:
        # start_str = input("Enter start date (YYYY-MM): ")
        try:
            start_str += "-01"
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format")
            continue
        # end_str = input("Enter end date (YYYY-MM): ")
        try:
            year, month = map(int, end_str.split("-"))
            _, max_days = calendar.monthrange(year, month)
            end_str += f"-{str(max_days)}"
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format")
            continue

    [print(exp) for exp in expenses if start_date <= datetime.strptime(exp["date"], "%Y-%m-%d").date() <= end_date]

def filter_by_amount(start_amount, end_amount):
    expenses = load_expenses()
    while True:
        # start_amount = input("Enter start amount: ")
        try:
            float(start_amount)
            break
        except ValueError:
            print("Invalid input")
    while True:
        # end_amount = input("Enter End amount: ")
        try:
            float(end_amount)
            break
        except ValueError:
            print("Invalid input")
    [print(exp) for exp in expenses if int(start_amount) <= int(exp.get("amount")) <= int(end_amount)]

#summary
def summary_by_month(month, year):
    expenses = load_expenses()
    while True:
        #month_str = input("Enter month (MM): ")
        try:
            # month = int(month_str)
            if 1 <= month <= 12:
                break
            else:
                print("Invalid month. Enter 01–12.")
        except ValueError:
            print("Invalid input. Please enter a number (01–12).")

    import calendar
    _, max_days = calendar.monthrange(year, month)

    start_date = date(year, month, 1)
    end_date = date(year, month, max_days)

    cost = sum([float(exp["amount"]) for exp in expenses if start_date <= datetime.strptime(exp["date"], "%Y-%m-%d").date() <= end_date])
    print(f"cost = {cost}")

def summary_by_category(category, year):
    expenses = load_expenses()
    # this_year = datetime.now().year
    # while True:
    #     for i, cat in enumerate(CATEGORIES, start=1):
    #         print(f"{i}. {cat}")
    #     choice = input("Enter number: ")
    #     if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
    #         category = CATEGORIES[int(choice)-1]
    #         break
    #     print("Invalid input. Try again.")
    cost = sum(float(exp["amount"]) for exp in expenses if exp["category"] == category and datetime.strptime(exp["date"], "%Y-%m-%d").year == year)
    print(f"cost of spending on {category} for the year {year} = {cost:.2f}")



def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--date", required=True, help="Date of expense (YYYY-MM-DD)")
    add_parser.add_argument("--category", required=True, help="Category of expense")
    add_parser.add_argument("--desc", required=True, help="Description of expense")
    add_parser.add_argument("--amount", required=True, type=float, help="Amount of expense")

    #edit command
    edit_parser = subparsers.add_parser("edit", help="edit expenses")
    edit_parser.add_argument("id", type=int, help="Expense ID to edit")
    edit_parser.add_argument("--date", required=False, help="Date of expense (YYYY-MM-DD)")
    edit_parser.add_argument("--category", required=False, help="Category of expense")
    edit_parser.add_argument("--desc", required=False, help="Description of expense")
    edit_parser.add_argument("--amount", required=False, type=float, help="Amount of expense")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("id", type=int, help="Expense ID to delete")

    # List expenses
    subparsers.add_parser("list", help="list down all expenses")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show summary of expenses")
    summary_parser.add_argument("-m", "--month", type=int, help="Month (1-12)")
    summary_parser.add_argument("-y", "--year", type=int, help="year (2025)")
    summary_parser.add_argument("-c", "--category", type=str, help="Filter by category")

    # Filter command
    filter_parser = subparsers.add_parser("filter", help="filters the list")
    filter_parser.add_argument("-d", "--date", nargs=2, metavar=("START", "END"), type=str, help="Filter by a start and end date (YYYY-MM-DD)")
    filter_parser.add_argument("-c", "--category", type=str, help="Filter by category")
    filter_parser.add_argument("-a", "--amount", nargs=2, metavar=("START", "END"), type=int, help="Filter by amount")
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.date, args.category, args.desc, args.amount)

    elif args.command == "edit":
        item_date = args.date if args.date else None
        category = verify_category(args.category) if args.category else None
        desc = args.desc if args.desc else None
        amount = args.amount if args.amount else None

        edit_expense(args.id, date=item_date, category=verify_category(category), desc=desc, amount=amount)

    elif args.command == "delete":
        delete_expense(args.id)

    elif args.command == "list":
        list_expenses()

    elif args.command == "summary":
        if args.month:
            summary_by_month(args.month, args.year or datetime.now().year)
        elif args.category:
            summary_by_category(verify_category(args.category), args.year or datetime.now().year)
        else:
            print("Please provide either --month/--year or --category")

    elif args.command == "filter":
        if args.date:
            start_date, end_date = args.date
            filter_by_date(start_date, end_date)
        elif args.category:
            filter_by_category(verify_category(args.category))
        elif args.amount:
            start_date, end_date = args.amount
            filter_by_amount(start_date, end_date)
        else:
            print("Please provide at least one filter (--date or --category or --amount).")

if __name__ == "__main__":
    main()