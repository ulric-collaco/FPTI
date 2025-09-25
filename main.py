
import os
from utils import read_transactions, read_balances, read_portfolio
from finance import monthly_cashflow, category_breakdown, print_monthly_report, plot_cashflow, plot_category_pie
from portfolio import value_portfolio, print_portfolio, print_net_worth


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    
    tx_file = os.path.join(data_dir, "transactions.csv")
    bal_file = os.path.join(data_dir, "balances.txt")
    port_file = os.path.join(data_dir, "portfolio.csv")

    if not os.path.exists(tx_file) or not os.path.exists(bal_file) or not os.path.exists(port_file):
        print("One or more data files are missing in " + data_dir)
        print("Expected: transactions.csv, balances.txt, portfolio.csv")
        return

    transactions = read_transactions(tx_file)
    balances = read_balances(bal_file)
    holdings = read_portfolio(port_file)

    income, expense, savings = monthly_cashflow(transactions)
    cat_totals = category_breakdown(transactions)

    holdings, portfolio_value = value_portfolio(holdings, True)

    print_monthly_report(income, expense, savings)
    print_net_worth(balances, portfolio_value)
    print_portfolio(holdings, portfolio_value)

    print("\nCategory-wise expense breakdown:")
    
    cat_items = []
    for cat in cat_totals:
        val = cat_totals[cat]
        cat_items.append((cat, val))
    
    for i in range(len(cat_items)):
        for j in range(i + 1, len(cat_items)):
            if cat_items[j][1] > cat_items[i][1]:
                temp = cat_items[i]
                cat_items[i] = cat_items[j]
                cat_items[j] = temp
    
    for cat, val in cat_items:
        print(cat + ": " + str(round(val, 2)))

    plot_cashflow(income, expense, True)
    plot_category_pie(cat_totals, True)


if __name__ == "__main__":
    main()

