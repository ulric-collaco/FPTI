
import matplotlib.pyplot as plt
from utils import Transaction


def monthly_cashflow(transactions):
    income = {}
    expense = {}

    for t in transactions:
        m = t.date.strftime("%Y-%m")
        if t.amount >= 0:
            if m in income:
                income[m] = income[m] + t.amount
            else:
                income[m] = t.amount
        else:
            if m in expense:
                expense[m] = expense[m] + (-t.amount)
            else:
                expense[m] = -t.amount

    all_months = []
    for month in income.keys():
        if month not in all_months:
            all_months.append(month)
    for month in expense.keys():
        if month not in all_months:
            all_months.append(month)
    months = sorted(all_months)
    
    savings = {}
    for m in months:
        income_amount = 0.0
        if m in income:
            income_amount = income[m]
        expense_amount = 0.0
        if m in expense:
            expense_amount = expense[m]
        savings[m] = income_amount - expense_amount
    return income, expense, savings


def category_breakdown(transactions):
    cat_totals = {}
    for t in transactions:
        if t.amount < 0:
            if t.category in cat_totals:
                cat_totals[t.category] = cat_totals[t.category] + (-t.amount)
            else:
                cat_totals[t.category] = -t.amount
    return cat_totals


def print_monthly_report(income, expense, savings):
    all_months = []
    for month in income.keys():
        if month not in all_months:
            all_months.append(month)
    for month in expense.keys():
        if month not in all_months:
            all_months.append(month)
    months = sorted(all_months)
    
    print("\nMonthly Cash Flow Report")
    print("Month       \tIncome\t\tExpenses\tSavings")
    print("----------------------------------------------------")
    for m in months:
        income_amount = 0.0
        if m in income:
            income_amount = income[m]
        expense_amount = 0.0
        if m in expense:
            expense_amount = expense[m]
        savings_amount = 0.0
        if m in savings:
            savings_amount = savings[m]
        print(m + "\t" + str(round(income_amount, 2)) + "\t\t" + str(round(expense_amount, 2)) + "\t\t" + str(round(savings_amount, 2)))


def plot_cashflow(income, expense, show=True, save=None):
    all_months = []
    for month in income.keys():
        if month not in all_months:
            all_months.append(month)
    for month in expense.keys():
        if month not in all_months:
            all_months.append(month)
    months = sorted(all_months)
    
    x = months
    y_income = []
    for m in x:
        if m in income:
            y_income.append(income[m])
        else:
            y_income.append(0.0)
    
    y_expense = []
    for m in x:
        if m in expense:
            y_expense.append(expense[m])
        else:
            y_expense.append(0.0)
    
    plt.figure(figsize=(8, 4))
    plt.plot(x, y_income, marker="o", label="Income")
    plt.plot(x, y_expense, marker="o", label="Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Income vs Expenses per Month")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    else:
        plt.close()


def plot_category_pie(category_totals, show=True, save=None):
    labels = []
    for key in category_totals.keys():
        labels.append(key)
    
    sizes = []
    for k in labels:
        sizes.append(category_totals[k])
    
    if len(sizes) == 0:
        print("No expense categories to plot.")
        return
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%.1f%%", startangle=140)
    plt.title("Expense by Category")
    plt.tight_layout()
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    else:
        plt.close()
