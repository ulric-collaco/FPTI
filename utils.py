"""Helpers: read transactions, balances, portfolio CSVs."""
import csv
from datetime import datetime


class Transaction:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category


class Holding:
    def __init__(self, symbol, quantity, price=0.0):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price


def read_transactions(path):
    txns = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            date_field = r.get("Date")
            if date_field is None:
                date_field = ""
            date_field = date_field.strip()
            
            # skip comment rows or empty date cells
            if not date_field or date_field.startswith("#"):
                continue
            
            try:
                date = datetime.fromisoformat(date_field)
            except:
                # skip rows with malformed dates
                continue
            
            desc = r.get("Description")
            if desc is None:
                desc = ""
            desc = desc.strip()
            
            try:
                amt = float(r.get("Amount", 0))
            except:
                amt = 0.0
            
            cat = r.get("Category")
            if cat is None:
                cat = "Uncategorized"
            cat = cat.strip()
            
            new_transaction = Transaction(date, desc, amt, cat)
            txns.append(new_transaction)
    return txns


def read_balances(path):
    balances = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                words = line.split()
                first_word = words[0]
                val = float(first_word)
                balances.append(val)
            except:
                continue
    return balances


def read_portfolio(path):
    holdings = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            sym = r.get("Symbol")
            if sym is None:
                sym = r.get("symbol")
            if not sym:
                continue
            sym = sym.strip()
            
            try:
                qty = float(r.get("Quantity", 0))
            except:
                qty = 0.0
            
            new_holding = Holding(sym, qty)
            holdings.append(new_holding)
    return holdings
