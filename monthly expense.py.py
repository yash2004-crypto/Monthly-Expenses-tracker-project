import json
import csv
import argparse
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage
import os


Category_keywords = {
    "Food": ["domino", "pizza", "restaurant", "uber eats", "zomato"],
    "Transport": ["uber", "lyft", "bus", "train", "taxi"],
    "Shopping": ["amazon", "flipkart", "myntra", "store"],
    "Utilities": ["electricity", "water", "gas", "internet", "wifi"],
    "Entertainment": ["netflix", "spotify", "cinema", "movie"],
    "Others": []
}



Default_Budget ={
    "Food": 25000,
    "Transport": 10000,
    "Shopping": 15000,
    "Utilities": 7000,
    "Entertainment":2000,
    "Others": 1500
}

TRANSACTION_FILE = "transactions.json"
OUTPUT_CSV = "monthly_expenses.csv"
REPORT_IMAGE = "expense_report.png"

def load_transactions():
    with open(TRANSACTION_FILE,"r") as file:
        data =json.load(file)
    return data

def categorize(description):
    desc = description.lower()
    for category , keywords in Category_keywords.items():
        if any(keyword in desc for keyword in keywords):
            return category
    return "Others"        

def calculate_expenses(transactions):
    expenses = defaultdict(float)
    now = datetime.datetime.now()
    for tx in transactions:
        date = datetime.datetime.strptime(tx["date"],"%Y-%m-%d")
        if date.month == now.month and date.year == now.year:
            category = categorize(tx["description"])
            expenses[category] += float(tx["amount"])
    return expenses

def save_to_csv(expenses):
    """Save categorized expenses to CSV"""
    with open(OUTPUT_CSV, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["category", "amount"])
        for cat, amt in expenses.items():
            writer.writerow([cat, amt])



def plot_pie_chart(expenses):
    """create and save a pie chart for expenses"""
    labels = expenses.keys()
    sizes = expenses.values()

    plt.figure(figsize=(6,6))
    plt.pie(sizes , labels = labels , autopct='%1.1f%%' , startangle= 140)
    plt.title("Monthly Expense Distribution")
    plt.savefig(REPORT_IMAGE)
    plt.close()


def send_email_report(expenses,budget):
    """Stimulate sending an email report and warning if limit exceeded"""
    message = "Daily Finance Tracker Report"
    warning = False

    for category, amount in expenses.items():
        budget_value =budget.get(category,0)
        message += f"{category}: ,${amount:.2f} /${budget_value:.2f}\n"
        if amount>0.5*budget_value:
            message += f"Warning:{category} spending is over 80% of your budget! \n"
            warning = True

    message += "\n (Report chart saved as 'expense_report.png')"  

    print(message)
    print("\n[Stimulated] Email report sent")
          
def parse_args(): 
    """Parse command-line arguments for custom budgets"""
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")
    for category in Default_Budget:
        parser.add_argument(f"--{category.lower()}", type=float, help= f"Monthly budget for {category}")
    return parser.parse_args()   



def main():
    args = parse_args()
    budgets = Default_Budget.copy()
    for category in Default_Budget:
        user_value = getattr(args , category.lower(),None)
        if user_value is not None:
            budgets[category]=user_value

    transactions = load_transactions()
    expenses = calculate_expenses(transactions)


    save_to_csv(expenses)
    plot_pie_chart(expenses)
    send_email_report(expenses,budgets)


if __name__ == "__main__":
    main()





          



 
      






