"""Core finance functions: cashflow, category breakdown, reporting, plotting."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from utils import Transaction


def monthly_cashflow(transactions: List[Transaction]) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
    income: Dict[str, float] = defaultdict(float)
    expense: Dict[str, float] = defaultdict(float)

    for t in transactions:
        m = t.date.strftime("%Y-%m")
        if t.amount >= 0:
            income[m] += t.amount
        else:
            expense[m] += -t.amount

    months = sorted(set(list(income.keys()) + list(expense.keys())))
    savings: Dict[str, float] = {}
    for m in months:
        savings[m] = income.get(m, 0.0) - expense.get(m, 0.0)
    return income, expense, savings


def category_breakdown(transactions: List[Transaction]) -> Dict[str, float]:
    cat_totals: Dict[str, float] = defaultdict(float)
    for t in transactions:
        if t.amount < 0:
            cat_totals[t.category] += -t.amount
    return dict(cat_totals)


def print_monthly_report(income: Dict[str, float], expense: Dict[str, float], savings: Dict[str, float]):
    months = sorted(set(list(income.keys()) + list(expense.keys())))
    print("\nMonthly Cash Flow Report")
    print("Month       \tIncome\t\tExpenses\tSavings")
    print("----------------------------------------------------")
    for m in months:
        print(f"{m}\t{income.get(m,0):10.2f}\t{expense.get(m,0):10.2f}\t{savings.get(m,0):10.2f}")


def plot_cashflow(income: Dict[str, float], expense: Dict[str, float], show: bool = True, save: Path | None = None):
    months = sorted(set(list(income.keys()) + list(expense.keys())))
    x = months
    y_income = [income.get(m, 0.0) for m in x]
    y_expense = [expense.get(m, 0.0) for m in x]
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


def plot_category_pie(category_totals: Dict[str, float], show: bool = True, save: Path | None = None):
    labels = list(category_totals.keys())
    sizes = [category_totals[k] for k in labels]
    if not sizes:
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
