import json
from datetime import datetime
import csv
import pandas as pd
import calendar
import requests

GET_CURL = 'https://script.google.com/macros/s/AKfycbz6nET9Q8Tjulg8tZuZTPzfhZfaLDPE7-FNDLx1oUM2tLHQQiv-_6OOc1241TbzGfnmKw/exec?header=con'
POST_CURL = 'https://script.google.com/macros/s/AKfycbwsfaiy4MujyCvoc50bZaKsqaX7BEkiNP9IMPBhQlQQ9mF4krZdpn8sPUQCTYWwurf1ww/exec'

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

def load_json():
    try:
        response = requests.get(GET_CURL)
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
        response = requests.post(POST_CURL, json=data, headers=headers)

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
            print(f'{i+1}. Spent {expense["amount"]} in {expense["category"]} with {expense["remarks"]}')
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

def menu():
    print("\n--Expense Tracker Menu--")
    print("1. Add Expenses")
    print("2. View Expense")
    print("3. Total Expense by Category")
    print("4. Export To CSV")
    print("5. Filter by Category")
    print("6. Filteration on Month OR Category")
    print("7. Exit")

def get_choice():
    while True:
        choice = input("Enter your Choice: ")
        if choice.isdigit():
            return int(choice)
        else:
            print("Enter a valid number")

if __name__ == "main":
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
            break

        else:
            print("Wrong Choice")