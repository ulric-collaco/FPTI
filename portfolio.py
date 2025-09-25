"""Portfolio functions: fetch prices (yfinance optional), value portfolio, print reports."""
from utils import Holding
import yfinance as yf



def _mock_prices(symbols):
    base = {
        "AAPL": 160.0,
        "TSLA": 220.0,
        "BTC-USD": 60000.0,
        "ETH-USD": 3500.0,
    }
    prices = {}
    for i in range(len(symbols)):
        s = symbols[i]
        if s in base:
            prices[s] = base[s]
        else:
            prices[s] = 20.0 + i * 5.0
    return prices


def fetch_prices(symbols, use_yfinance=True):
    prices = {}
    if use_yfinance:
        try:
            symbol_string = " ".join(symbols)
            tickers = yf.Tickers(symbol_string)
            for sym in symbols:
                try:
                    tk = tickers.tickers.get(sym)
                    if tk is None:
                        prices[sym] = 0.0
                        continue
                    info = tk.history(period="1d")
                    if not info.empty:
                        last_close = info["Close"].iloc[-1]
                        prices[sym] = float(last_close)
                    else:
                        market_price = tk.info.get("regularMarketPrice", 0.0)
                        if market_price is None:
                            market_price = 0.0
                        prices[sym] = float(market_price)
                except:
                    prices[sym] = 0.0
        except:
            # If the network or yfinance raises, fall back to mock prices
            prices = _mock_prices(symbols)
    else:
        prices = _mock_prices(symbols)
    return prices


def value_portfolio(holdings, use_yfinance=True):
    syms = []
    for h in holdings:
        syms.append(h.symbol)
    prices = fetch_prices(syms, use_yfinance)
    total = 0.0
    for h in holdings:
        if h.symbol in prices:
            p = prices[h.symbol]
        else:
            p = 0.0
        h.price = p
        total = total + (p * h.quantity)
    return holdings, total


def compute_net_worth(balances, portfolio_value):
    total_balances = 0.0
    for balance in balances:
        total_balances = total_balances + balance
    return total_balances + portfolio_value


def print_portfolio(holdings, total_value):
    print("\nPortfolio Details")
    print("Symbol\tQuantity\tPrice\tValue")
    print("-------------------------------------------")
    for h in holdings:
        value = h.price * h.quantity
        print(h.symbol + "\t" + str(round(h.quantity, 4)) + "\t" + str(round(h.price, 2)) + "\t" + str(round(value, 2)))
    print("Total portfolio value: " + str(round(total_value, 2)))


def print_net_worth(balances, portfolio_value):
    print("\nNet Worth")
    for i in range(len(balances)):
        b = balances[i]
        balance_number = i + 1
        print("Balance " + str(balance_number) + ": " + str(round(b, 2)))
    
    total_balances = 0.0
    for balance in balances:
        total_balances = total_balances + balance
    
    print("Total cash/balances: " + str(round(total_balances, 2)))
    print("Portfolio value: " + str(round(portfolio_value, 2)))
    
    net_worth = compute_net_worth(balances, portfolio_value)
    print("TOTAL net worth: " + str(round(net_worth, 2)))
