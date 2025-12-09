import json
from datetime import datetime
import csv
import pandas as pd
import calendar
import requests

CURL = 'https://script.google.com/macros/s/AKfycbxdg7VughSCeY_GUZtMUYZnPs1SwUbpG-aDUOfPKka8gmBzb3g4NR49nU3djWPWCf9jcQ/exec'

ALLOWED_CATEGORIES = [
    "Snacks",
    "Food",
    "Transport",
    "House Utilities",
    "Groceries",
    "Rent",
    "Mobile/Internet",
    "Entertainment",
    "Shopping",
    "Health",
    "Education",
    "Others"
    ]

Month_Name = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

update_fields = [
    "amount",
    "category",
    "remarks",
    "date"
]

def load_json():
    try:
        response = requests.get(CURL)
        response.raise_for_status()

        api_data = response.json()
        return api_data.get("data",[]) 
    

    except Exception as E:
        print(f"Something went wrong: {E}")
        return []

def write_json(data):
    try:
        # Define the URL and payload
        headers = {"Content-Type": "application/json"}

        # Send a POST request
        response = requests.post(CURL, json=data, headers=headers)

        # Print the response
        if response.status_code == 200:
            # print("Response:", response.json())
            return response.json()
        else:
            print("Error:", response.text)
    except Exception as E:
        print(f"Something went wrong: {E}")

def choose_category():
    for i, value in enumerate(ALLOWED_CATEGORIES):
        print(f"{i+1}. {value}")
    while True:
        choice_cat = int(input("Enter category number: "))
        if choice_cat >= 1 and choice_cat <= len(ALLOWED_CATEGORIES):
            category = ALLOWED_CATEGORIES[choice_cat-1]
            print(f"Your chosen category is {category}")
            return category
        else:
            print(f"Invalid category.")
            print(f"Kindly choose a number between 1 and {len(ALLOWED_CATEGORIES)}")

def choose_month():
    for i, value in enumerate(Month_Name):
        print(f"{i+1}. {value}")
    while True:
        choice_cat = int(input("Enter month number: "))
        if choice_cat >= 1 and choice_cat <= len(Month_Name):
            MONTH = Month_Name[choice_cat-1]
            print(f"Your chosen Month is {MONTH}")
            return MONTH
        else:
            print(f"Invalid category.")
            print(f"Kindly choose a number between 1 and {len(Month_Name)}")

def get_positive_amt():
    while True:
        amount = input("Enter the Amount: ")

        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        else:
            print("Kindly Enter valid amount")

def add_expense():
    try:
        amount = get_positive_amt()
        print(f"\n Choose a category.")
        category = choose_category()
        remarks = input("Enter your notes: ")

        new_expense = {
            "amount" : amount,
            "category" : category,
            "remarks" : remarks,
            "date" : datetime.now().strftime("%Y-%m-%d")
        }
        
        response = write_json(new_expense)

        if response["message"] == 'Expense already exists':
            print("Expense is already added")
        else:
            print("Expense Added")
        
    except Exception as e:
        print(f"Something went Wrong: {e}")

def view_expenses():
    data = load_json()
    try:
        print("All Expense: ")
        for i,expense in enumerate(data):
            print(f'{expense["ID"]}. Spent {expense["amount"]} in {expense["category"]} with {expense["remarks"]}')
    except Exception as E:
        print(f"Something went wrong: {E}")

def expense_by_category():
    data = load_json()
    categoryWiseExpenses = {}

    for expense in data:
        if expense["category"] in categoryWiseExpenses.keys():
            categoryWiseExpenses[expense["category"]] += expense["amount"]
        else:
            categoryWiseExpenses[expense["category"]] = expense["amount"]

    for key,value in categoryWiseExpenses.items():
        print(f"{key} -> {value}")

def expost_to_csv():
    data = load_json()
    with open("output.csv","w", newline="") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames= ["amount", "category", "remarks","date"])
        writer.writeheader()
        writer.writerows(data)
    print("Data written and exported to csv")

def filter_by_category(filteredCategory):
    cnt = 0
    data = load_json()
    for expense in data:
        if filteredCategory.lower() == expense['category'].lower():
            cnt +=1
            print(f"For {filteredCategory} category, {cnt}. {expense['amount']} on {expense['date']} with note {expense['remarks']}")
    if cnt == 0:
        print(f"No expense have been made for {filteredCategory}")

def filter_month_category(monthName = None, Category = None):
    user_input =int(input("\nOn What Basis would you like to filter data?\n Type 1 if you want Month Level Filteration.\n Type 2 if you want Category Level Filteration.\n Type 3 if you want both Month & Category Level Filteration.: "))

    if user_input == 1:
        monthName = choose_month()
    elif user_input == 2:
        Category = choose_category()
    elif user_input == 3:
        monthName = choose_month()
        Category = choose_category()
    
    data = load_json()
    filtered = []
    if monthName != None and Category != None:
        for expense in data:
            if (monthName == calendar.month_name[datetime.strptime(expense['date'],"%Y-%m-%d").month]) and (Category == expense['category']):
                filtered.append(expense)
    
    elif monthName != None:
        for expense in data:
            if (monthName == calendar.month_name[datetime.strptime(expense['date'],"%Y-%m-%d").month]):
                filtered.append(expense)

    elif Category != None:
        for expense in data:
            if (Category == expense['category']):
                filtered.append(expense)

    return filtered

def choose_field_to_update():
    print("Select fields you want to update:")
    print("\nWhich fields do you want to update?")
    for i,field in enumerate(update_fields,1):
        print(f"{i}. {field}")
    print("0. Done Selecting")

    selected_fields = []
    while True:
        choose_field = input("Enter field number (or 0 to finish): ")

        if choose_field.isdigit():
            choose_field = int(choose_field)

            if choose_field == 0:
                break

            elif choose_field > 0 and choose_field <= len(update_fields):
                field_name = update_fields[choose_field-1]
                if field_name not in selected_fields:
                    selected_fields.append(field_name)
                else:
                    print("Already Added")
            else:
                print("Invalid Choice")
        else:
            print("Enter a valid number")

    return selected_fields


def get_new_value(field):
    if field == 'amount':
        amount = get_positive_amt()
        return amount
    
    elif field == 'category':
        category = choose_category()
        return category
    
    elif field == 'date':
        date = input("Enter date in YYYY-MM-DD format: ")
        return date

    elif field =='remarks':
        remarks = input("Enter Remarks: ")
        return remarks

def update_expense():
    view_expenses()

    ID = int(input("Enter the ID of the expense you want to update: "))

    data = load_json()
    expense_to_update = {}
    for expense in data:
        if ID == expense["ID"]:
            expense_to_update = expense
            break
    
    if expense_to_update == {}:
        print(f"No expense found with {ID} ID")
        return

    field_to_update = choose_field_to_update()

    updated_data = {
        "method" : "update",
        "ID" : expense_to_update["ID"] 
    }

    for key in update_fields:
        updated_data[key] = expense_to_update[key]

    for field in field_to_update:
        new_value = get_new_value(field)
        updated_data[field] = new_value

    response = write_json(updated_data)

    print("Updated Expense") 
    print(f"{updated_data['ID']} || {updated_data['amount']} || {updated_data['remarks']} || {updated_data['category']} || {updated_data['date']}")


def delete_expense():
    view_expenses()

    ID = int(input("Enter the ID of the expense you want to delete: "))

    data = load_json()
    expense_to_delete = {}
    for expense in data:
        if ID == expense["ID"]:
            expense_to_delete = expense
            break
    
    if expense_to_delete ==  {}:
        print(f"No expense found with {ID} ID")
        return
    
    update_expense = {
        "method" : "delete",
        "ID" : expense_to_delete["ID"]
    }

    response = write_json(update_expense)

    view_expenses()



def menu():
    print("\n--Expense Tracker Menu--")
    print("1. Add Expenses")
    print("2. View Expense")
    print("3. Total Expense by Category")
    print("4. Export To CSV")
    print("5. Filter by Category")
    print("6. Filteration on Month OR Category")
    print("7. Update an Expense")
    print("8. Delete an Expense")
    print("9. Exit")

def get_choice():
    while True:
        choice = input("Enter your Choice: ")
        if choice.isdigit():
            return int(choice)
        else:
            print("Enter a valid number")


if __name__ == "__main__":
    while True:
        menu()
        choice = get_choice()

        if choice == 1:
            add_expense()

        elif choice == 2:
            view_expenses()
            

        elif choice == 3:
            expense_by_category()

        elif choice == 4:
            expost_to_csv()

        elif choice == 5:
            category = choose_category()
            filter_by_category(category)

        elif choice == 6:
            result = filter_month_category()
            for i, exp in enumerate(result, 1):
                print(f"{i}. {exp['amount']} | {exp['category']} | {exp['remarks']} | {exp['date']}")

        elif choice == 7:
            update_expense()

        elif choice == 8:
            delete_expense()

        elif choice == 9:
            break

        else:
            print("Wrong Choice")
