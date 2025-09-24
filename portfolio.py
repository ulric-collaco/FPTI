"""Portfolio functions: fetch prices (yfinance optional), value portfolio, print reports."""
from __future__ import annotations
from typing import Dict, List, Tuple

from utils import Holding
import yfinance as yf



def _mock_prices(symbols: List[str]) -> Dict[str, float]:
    base = {
        "AAPL": 160.0,
        "TSLA": 220.0,
        "BTC-USD": 60000.0,
        "ETH-USD": 3500.0,
    }
    prices = {}
    for i, s in enumerate(symbols):
        prices[s] = base.get(s, 20.0 + i * 5.0)
    return prices


def fetch_prices(symbols: List[str], use_yfinance: bool = True) -> Dict[str, float]:
    prices = {}
    if use_yfinance:
        try:
            tickers = yf.Tickers(" ".join(symbols))
            for sym in symbols:
                try:
                    tk = tickers.tickers.get(sym)
                    if tk is None:
                        prices[sym] = 0.0
                        continue
                    info = tk.history(period="1d")
                    if not info.empty:
                        prices[sym] = float(info["Close"].iloc[-1])
                    else:
                        prices[sym] = float(tk.info.get("regularMarketPrice", 0.0) or 0.0)
                except Exception:
                    prices[sym] = 0.0
        except Exception:
            # If the network or yfinance raises, fall back to mock prices
            prices = _mock_prices(symbols)
    else:
        prices = _mock_prices(symbols)
    return prices


def value_portfolio(holdings: List[Holding], use_yfinance: bool = True) -> Tuple[List[Holding], float]:
    syms = [h.symbol for h in holdings]
    prices = fetch_prices(syms, use_yfinance=use_yfinance)
    total = 0.0
    for h in holdings:
        p = prices.get(h.symbol, 0.0)
        h.price = p
        total += p * h.quantity
    return holdings, total


def compute_net_worth(balances: List[float], portfolio_value: float) -> float:
    return sum(balances) + portfolio_value


def print_portfolio(holdings: List[Holding], total_value: float):
    print("\nPortfolio Details")
    print("Symbol\tQuantity\tPrice\tValue")
    print("-------------------------------------------")
    for h in holdings:
        print(f"{h.symbol}\t{h.quantity:.4f}\t{h.price:,.2f}\t{h.price * h.quantity:,.2f}")
    print(f"Total portfolio value: {total_value:,.2f}")


def print_net_worth(balances: List[float], portfolio_value: float):
    print("\nNet Worth")
    for i, b in enumerate(balances, start=1):
        print(f"Balance {i}: {b:,.2f}")
    print(f"Total cash/balances: {sum(balances):,.2f}")
    print(f"Portfolio value: {portfolio_value:,.2f}")
    print(f"TOTAL net worth: {compute_net_worth(balances, portfolio_value):,.2f}")
