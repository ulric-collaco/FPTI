# Personal Finance Dashboard (CLI)

A small command-line personal finance dashboard that reads local CSV/TXT data and prints reports and plots.

Features
- Monthly cashflow (income, expenses, savings)
- Category-wise expense breakdown
- Portfolio valuation (fetches live prices via `yfinance` when available)
- Net worth calculation (cash balances + portfolio)
- Plots: income vs expenses (line), expense distribution (pie)

Requirements
- Python 3.10+
- Recommended (install with pip):
  ```powershell
  pip install -r personal_finance\requirements.txt
  ```

Files
- `personal_finance/main.py` - CLI entry point (runs without flags; always attempts live fetch and shows plots)
- `personal_finance/finance.py` - cashflow and plotting helpers
- `personal_finance/portfolio.py` - portfolio valuation and price fetching (yfinance optional)
- `personal_finance/utils.py` - file parsing helpers
- `personal_finance/data/transactions.csv` - sample transactions (12+ months)
- `personal_finance/data/portfolio.csv` - sample holdings
- `personal_finance/data/balances.txt` - sample balances

Usage
Run from the repository root (where the `personal_finance` folder lives):

Show reports and plots (attempt live prices via yfinance):
```powershell
python .\personal_finance\main.py
```

Run without network (yfinance not installed) — the script will use deterministic mock prices:
```powershell
python .\personal_finance\main.py
```

Headless server: suppress interactive plotting by setting a non-interactive backend or editing the code to use `Agg`. Example (PowerShell temporary env var):
```powershell
$env:MPLBACKEND='Agg'; python .\personal_finance\main.py
```

Customization
- To change data files, replace the CSV/TXT files in `personal_finance/data/`.
- The `portfolio.py` module uses `yfinance` if available and falls back to mock prices otherwise.

Notes
- The script currently always attempts to fetch live prices and always shows plots. If you want CLI flags to opt out, ask me and I can reintroduce them.

License
MIT-style: free to modify and use.
