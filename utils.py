"""Helpers: read transactions, balances, portfolio CSVs."""
from __future__ import annotations
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class Transaction:
    date: datetime
    description: str
    amount: float
    category: str


@dataclass
class Holding:
    symbol: str
    quantity: float
    price: float = 0.0


def read_transactions(path: Path) -> List[Transaction]:
    txns: List[Transaction] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            date_field = (r.get("Date") or "").strip()
            # skip comment rows or empty date cells
            if not date_field or date_field.startswith("#"):
                continue
            try:
                date = datetime.fromisoformat(date_field)
            except Exception:
                # skip rows with malformed dates
                continue
            desc = r.get("Description", "").strip()
            try:
                amt = float(r.get("Amount", 0))
            except ValueError:
                amt = 0.0
            cat = r.get("Category", "Uncategorized").strip()
            txns.append(Transaction(date=date, description=desc, amount=amt, category=cat))
    return txns


def read_balances(path: Path) -> List[float]:
    balances = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                token = line.split()[0]
                val = float(token)
                balances.append(val)
            except Exception:
                continue
    return balances


def read_portfolio(path: Path) -> List[Holding]:
    holdings: List[Holding] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            sym = r.get("Symbol") or r.get("symbol")
            if not sym:
                continue
            sym = sym.strip()
            try:
                qty = float(r.get("Quantity", 0))
            except Exception:
                qty = 0.0
            holdings.append(Holding(symbol=sym, quantity=qty))
    return holdings
