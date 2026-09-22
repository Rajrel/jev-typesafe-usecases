"""Read the Northwind sample shop: SQLite, JSON fixtures, and the doc corpus."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from jev_examples.settings import repo_root


def data_dir() -> Path:
    return repo_root() / "data"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(data_dir() / "shop.db")
    connection.row_factory = sqlite3.Row
    return connection


def rows(sql: str, params: tuple = ()) -> list[dict]:
    with connect() as connection:
        return [dict(row) for row in connection.execute(sql, params)]


def ticket(ticket_id: str) -> dict:
    found = rows(
        """
        SELECT t.*,
               c.name AS customer_name,
               c.email AS customer_email,
               o.status AS order_status,
               o.total_usd,
               o.days_since_purchase,
               o.charge_count
        FROM support_tickets t
        LEFT JOIN customers c ON c.id = t.customer_id
        LEFT JOIN orders o ON o.id = t.order_id
        WHERE t.id = ?
        """,
        (ticket_id,),
    )
    if not found:
        raise KeyError(ticket_id)
    return found[0]


def order(order_id: str) -> dict:
    found = rows(
        """
        SELECT o.*, c.name AS customer_name, c.email AS customer_email
        FROM orders o
        JOIN customers c ON c.id = o.customer_id
        WHERE o.id = ?
        """,
        (order_id,),
    )
    if not found:
        raise KeyError(order_id)
    record = found[0]
    record["lines"] = rows(
        "SELECT sku, description, amount_usd FROM order_lines WHERE order_id = ?",
        (order_id,),
    )
    return record


def tickets() -> list[dict]:
    return rows("SELECT id, subject, body FROM support_tickets ORDER BY id")


def emails() -> list[dict]:
    return rows(
        "SELECT id, sender_name, sender_email, subject, body, folder FROM emails ORDER BY id"
    )


def open_incidents() -> list[dict]:
    return rows(
        "SELECT id, title, status, customer_impact, summary FROM incidents WHERE status = 'open'"
    )


def products() -> list[dict]:
    return rows("SELECT sku, name, category_path, description, price_usd FROM products")


def customers() -> list[dict]:
    return rows("SELECT id, name, email, city, segment, notes FROM customers")


def lookup_order(order_id: str) -> str:
    record = order(order_id)
    lines = ", ".join(line["description"] for line in record["lines"])
    return (
        f"{record['id']} for {record['customer_name']}: {record['status']}, "
        f"${record['total_usd']:.2f}, {record['days_since_purchase']} days since purchase. "
        f"Items: {lines}."
    )


def load_json(name: str):
    path = data_dir() / "fixtures" / name
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(name: str) -> str:
    path = data_dir() / "fixtures" / name
    if not path.exists():
        path = data_dir() / "corpus" / name
    return path.read_text(encoding="utf-8")


def corpus_docs() -> list[dict]:
    docs = []
    for path in sorted((data_dir() / "corpus").glob("*.md")):
        docs.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
    return docs
