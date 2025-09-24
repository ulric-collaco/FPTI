"""Personal Finance Dashboard CLI.

Reads data from the local data/ directory and prints reports + plots.
"""

from __future__ import annotations
from pathlib import Path

from utils import read_transactions, read_balances, read_portfolio
from finance import monthly_cashflow, category_breakdown, print_monthly_report, plot_cashflow, plot_category_pie
from portfolio import value_portfolio, print_portfolio, print_net_worth


DATA_DIR = Path(__file__).parent / "data"


def main():
    data_dir = Path(DATA_DIR)
    tx_file = data_dir / "transactions.csv"
    bal_file = data_dir / "balances.txt"
    port_file = data_dir / "portfolio.csv"

    # Check data files
    if not tx_file.exists() or not bal_file.exists() or not port_file.exists():
        print("One or more data files are missing in", data_dir)
        print("Expected: transactions.csv, balances.txt, portfolio.csv")
        return

    # Read data
    transactions = read_transactions(tx_file)
    balances = read_balances(bal_file)
    holdings = read_portfolio(port_file)

    # Reports
    income, expense, savings = monthly_cashflow(transactions)
    cat_totals = category_breakdown(transactions)

    # Always attempt to fetch live prices (portfolio module falls back to mock prices internally)
    holdings, portfolio_value = value_portfolio(holdings, use_yfinance=True)

    # Print reports
    print_monthly_report(income, expense, savings)
    print_net_worth(balances, portfolio_value)
    print_portfolio(holdings, portfolio_value)

    # Category breakdown
    print("\nCategory-wise expense breakdown:")
    for cat, val in sorted(cat_totals.items(), key=lambda x: -x[1]):
        print(f"{cat}: {val:,.2f}")

    # Always show plots
    plot_cashflow(income, expense, show=True)
    plot_category_pie(cat_totals, show=True)


if __name__ == "__main__":
    main()

