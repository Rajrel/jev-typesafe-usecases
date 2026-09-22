"""Rebuild data/shop.db for the Northwind Outfitters notebooks.

Run from the repo root:

    uv run python data/build_sample_db.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "shop.db"

CUSTOMERS = [
    ("C01", "Maya Chen", "maya.chen@example.com", "Seattle", "retail", "Prefers email."),
    ("C02", "Luis Ortega", "luis.ortega@example.com", "Austin", "retail", "Asked about trail shipping before."),
    ("C03", "Priya Shah", "priya.shah@example.com", "Chicago", "wholesale", "Buys tents for a summer camp."),
    ("C04", "Owen Blake", "owen.blake@example.com", "Denver", "retail", ""),
    ("C05", "Hannah Kim", "hannah.kim@example.com", "Portland", "retail", "Looking at packs, has not ordered."),
    ("C06", "Samir Patel", "samir.patel@example.com", "Boston", "retail", ""),
    ("C07", "Elena Rossi", "elena.rossi@example.com", "Miami", "retail", ""),
    ("C08", "Jonah Brooks", "jonah.brooks@example.com", "Denver", "retail", "Trail runner. Ships to 14 Pine St."),
    ("C09", "J. Brooks", "j.brooks@example.net", "Denver", "retail", "Same street as Jonah: 14 Pine St. Trail runner."),
    ("C10", "Northwind Ops", "ops@northwind.example", "Seattle", "internal", "Warehouse desk, not a shopper."),
    ("C11", "Test User", "test@test.com", "Testville", "test", "Placeholder account created by QA."),
    ("C12", "Acme Holdings", "ap@acme.example", "New York", "wholesale", "Company account, net 30."),
    ("C13", "Grace Nguyen", "grace.nguyen@example.com", "San Jose", "retail", ""),
    ("C14", "Theo Martin", "theo.martin@example.com", "Minneapolis", "retail", ""),
    ("C15", "Aisha Rahman", "aisha.rahman@example.com", "Atlanta", "retail", ""),
    ("C16", "Ben Carter", "ben.carter@example.com", "Boulder", "retail", ""),
    ("C17", "Nora Lind", "nora.lind@example.com", "Madison", "retail", ""),
    ("C18", "Chris Hale", "chris.hale@example.com", "Boise", "retail", ""),
]

PRODUCTS = [
    ("BTL-32", "32oz bike bottle", "Sporting Goods > Cycling", "Plastic bottle with a flip straw. Fits most bike cages.", 18),
    ("MUG-16", "16oz travel mug", "Home & Kitchen > Drinkware", "Insulated mug for coffee. Leakproof lid.", 24),
    ("TNT-2P", "Two-person tent", "Sporting Goods > Outdoor", "Freestanding tent for weekend trips.", 189),
    ("YOG-01", "Yoga mat", "Sporting Goods > Fitness", "6mm mat, rolls small.", 32),
    ("HLM-01", "Bike helmet", "Sporting Goods > Cycling", "Ventilated helmet, size medium.", 64),
    ("SLP-01", "Sleeping bag", "Sporting Goods > Outdoor", "Rated to 30F.", 99),
    ("TUM-20", "20oz tumbler", "Home & Kitchen > Drinkware", "Steel tumbler with a straw lid.", 28),
    ("BAK-01", "Sheet pan", "Home & Kitchen > Cookware", "Half-size aluminum sheet pan.", 22),
    ("SIP-01", "Sippy cup", "Baby & Toddler", "Spill-proof cup for toddlers.", 12),
    ("HYD-01", "Hydration pack", "Sporting Goods > Outdoor", "2 liter bladder and a small pack.", 54),
    ("PAK-40", "40L backpack", "Sporting Goods > Outdoor", "Weekend pack with a rain cover.", 120),
    ("SOK-01", "Wool socks", "Sporting Goods > Outdoor", "Pair of merino hiking socks.", 16),
    ("JKT-01", "Rain jacket", "Sporting Goods > Outdoor", "Packable shell, size medium.", 88),
    ("STV-01", "Camp stove", "Sporting Goods > Outdoor", "Canister stove. Fuel sold separately.", 42),
    ("BND-01", "Resistance bands", "Sporting Goods > Fitness", "Set of three loop bands.", 20),
    ("WTR-24", "24oz water bottle", "Home & Kitchen > Drinkware", "Everyday bottle. Does not fit a bike cage.", 20),
]

ORDERS = [
    ("A-104", "C01", "delivered", 6, 98, 2, "2026-09-16"),
    ("A-118", "C02", "shipped", 21, 189, 1, "2026-09-01"),
    ("A-201", "C03", "delivered", 10, 378, 1, "2026-09-12"),
    ("A-220", "C04", "delivered", 40, 64, 1, "2026-08-13"),
    ("A-250", "C06", "delivered", 12, 16, 1, "2026-09-10"),
    ("A-260", "C07", "delivered", 4, 189, 1, "2026-09-18"),
    ("A-270", "C08", "delivered", 15, 120, 1, "2026-09-07"),
    ("A-280", "C13", "delivered", 8, 88, 1, "2026-09-14"),
    ("A-290", "C14", "processing", 2, 54, 1, "2026-09-20"),
    ("A-300", "C15", "delivered", 30, 99, 1, "2026-08-23"),
    ("A-310", "C16", "cancelled", 3, 42, 0, "2026-09-19"),
    ("A-320", "C17", "delivered", 18, 52, 1, "2026-09-04"),
    ("A-330", "C18", "delivered", 45, 24, 1, "2026-08-08"),
    ("A-340", "C12", "delivered", 9, 240, 1, "2026-09-13"),
    ("A-350", "C05", "draft", 0, 0, 0, "2026-09-21"),
    ("A-360", "C01", "delivered", 60, 50, 1, "2026-07-24"),
    ("A-370", "C09", "delivered", 15, 18, 1, "2026-09-07"),
    ("A-380", "C06", "shipped", 5, 64, 1, "2026-09-17"),
    ("A-390", "C03", "delivered", 22, 99, 1, "2026-08-31"),
    ("A-400", "C15", "delivered", 1, 20, 1, "2026-09-21"),
]

ORDER_LINES = [
    ("A-104", "BTL-32", "32oz bike bottle", 49),
    ("A-104", "BTL-32", "32oz bike bottle", 49),
    ("A-118", "TNT-2P", "Two-person tent", 189),
    ("A-201", "TNT-2P", "Two-person tent", 189),
    ("A-201", "TNT-2P", "Two-person tent", 189),
    ("A-220", "HLM-01", "Bike helmet", 64),
    ("A-250", "SOK-01", "Wool socks", 16),
    ("A-260", "TNT-2P", "Two-person tent", 189),
    ("A-270", "PAK-40", "40L backpack", 120),
    ("A-280", "JKT-01", "Rain jacket", 88),
    ("A-290", "HYD-01", "Hydration pack", 54),
    ("A-300", "SLP-01", "Sleeping bag", 99),
    ("A-310", "STV-01", "Camp stove", 42),
    ("A-320", "YOG-01", "Yoga mat", 32),
    ("A-330", "MUG-16", "16oz travel mug", 24),
    ("A-340", "PAK-40", "40L backpack", 120),
    ("A-340", "PAK-40", "40L backpack", 120),
    ("A-360", "BAK-01", "Sheet pan", 22),
    ("A-370", "BTL-32", "32oz bike bottle", 18),
    ("A-380", "HLM-01", "Bike helmet", 64),
    ("A-390", "SLP-01", "Sleeping bag", 99),
    ("A-400", "WTR-24", "24oz water bottle", 20),
    ("A-320", "BND-01", "Resistance bands", 20),
    ("A-360", "TUM-20", "20oz tumbler", 28),
]

TICKETS = [
    ("T-104", "C01", "A-104", "Charged twice", "I was charged twice for order A-104. Both charges are $49. I want the extra charge refunded today.", "email", "2026-09-20"),
    ("T-118", "C02", "A-118", "Where is my tent", "Hi, can you tell me where order A-118 is? It has been three weeks. No rush if you need a day to check.", "email", "2026-09-21"),
    ("T-201", "C03", "A-201", "Refund for camp tents", "Please refund order A-201. The tents arrived with broken poles and we are still inside the 30 day window.", "email", "2026-09-21"),
    ("T-220", "C04", "A-220", "Cannot log in", "I cannot log in to my account. The reset email never arrives. I am not asking about a charge.", "chat", "2026-09-18"),
    ("T-250", "C06", "A-250", "Socks have a hole", "The wool socks from A-250 have a hole in the heel. I would like an exchange, not a long argument.", "email", "2026-09-19"),
    ("T-260", "C07", "A-260", "Tent is missing", "THIS IS UNACCEPTABLE. Order A-260 says delivered and there is no tent. I have called twice. Fix this now.", "phone", "2026-09-21"),
    ("T-270", "C05", None, "Is the 40L pack waterproof", "Before I buy, does the 40L backpack include a rain cover and will it fit a 2 liter bladder?", "chat", "2026-09-21"),
    ("T-280", "C13", "A-280", "Jacket size", "The rain jacket on A-280 is too small. I want to exchange it for a large. I bought it 8 days ago.", "email", "2026-09-20"),
    ("T-290", "C14", "A-290", "Cancel hydration pack", "Please cancel order A-290 if it has not shipped. I ordered the wrong pack.", "chat", "2026-09-21"),
    ("T-300", "C15", "A-300", "Sleeping bag zipper", "The zipper on the sleeping bag sticks. It is annoying but I can still use the bag. Just letting you know.", "email", "2026-09-15"),
    ("T-310", "C16", "A-310", "Stove cancelled but charged", "You cancelled A-310 and I still see a pending charge. Please confirm it will drop off.", "email", "2026-09-20"),
    ("T-320", "C17", "A-320", "Mat smells", "The yoga mat smells like chemicals. Is that normal for the first week?", "chat", "2026-09-16"),
    ("T-330", "C18", "A-330", "Mug refund", "I want a refund on the travel mug from A-330. I bought it about six weeks ago and the lid leaks.", "email", "2026-09-21"),
    ("T-340", "C12", "A-340", "Wholesale invoice", "Please send the invoice for A-340 to ap@acme.example. We need it for our net 30 payment.", "email", "2026-09-18"),
    ("T-350", "C08", "A-270", "Pack strap", "The chest strap on my 40L pack frays after one hike. What is the warranty?", "email", "2026-09-19"),
    ("T-360", "C10", None, "Checkout errors", "Customers are seeing 500 errors on checkout since the Friday deploy. This is the same outage as the open incident.", "internal", "2026-09-21"),
    ("T-370", "C11", None, "New feature idea", "It would be nice if the site remembered my tent size. Not urgent, just an idea.", "chat", "2026-09-17"),
    ("T-380", "C09", "A-370", "Bottle cage fit", "The 32oz bottle fits my cage. Thanks. You can close this note.", "email", "2026-09-18"),
]

EMAILS = [
    ("E01", "Maya Chen", "maya.chen@example.com", "Double charge", "I was charged twice for A-104. Please refund one $49 charge today.", "inbox"),
    ("E02", "Luis Ortega", "luis.ortega@example.com", "Tracking", "Could you send tracking for the tent when you have a moment this week?", "inbox"),
    ("E03", "Priya Shah", "priya.shah@example.com", "Approve the replacement", "Please decide today if you will replace the broken tent poles. Camp starts Monday.", "inbox"),
    ("E04", "Warehouse Lead", "lead@northwind.example", "Sign off on cycle count", "Need your approval on the September cycle count before we close the books tonight.", "inbox"),
    ("E05", "Newsletter", "news@trailmail.example", "October trails", "Ten fall hikes near you. Unsubscribe any time.", "inbox"),
    ("E06", "Owen Blake", "owen.blake@example.com", "Password", "I still cannot log in. Can someone reset the account this week?", "inbox"),
    ("E07", "Elena Rossi", "elena.rossi@example.com", "Where is the tent", "The tracking page says delivered. The tent is not here. Please call me today.", "inbox"),
    ("E08", "Grace Nguyen", "grace.nguyen@example.com", "Exchange jacket", "Schedule an exchange for a size large jacket whenever a slot is open.", "inbox"),
    ("E09", "Ben Carter", "ben.carter@example.com", "Thanks", "The stove cancellation looks correct. No reply needed.", "inbox"),
    ("E10", "Acme Holdings", "ap@acme.example", "Net 30 copy", "Please send a copy of invoice INV-2044 to our accounts payable alias.", "inbox"),
    ("E11", "Samir Patel", "samir.patel@example.com", "Hole in socks", "The socks have a hole. I would like a replacement pair.", "inbox"),
    ("E12", "Aisha Rahman", "aisha.rahman@example.com", "Zipper", "The sleeping bag zipper sticks. Not urgent.", "inbox"),
    ("E13", "Unknown", "prize@claim-bonus.example", "You won a tent", "Congratulations, your prize tent is ready. Reply with your password so we can release it.", "inbox"),
    ("E14", "Northwind Ops", "ops@northwind.example", "Deploy note", "Friday's checkout deploy is the one tied to the 500 errors. Internal only.", "sent"),
    ("E15", "Hannah Kim", "hannah.kim@example.com", "Pack question", "Does the 40L pack include a rain cover?", "inbox"),
    ("E16", "Theo Martin", "theo.martin@example.com", "Cancel pack", "Please cancel the hydration pack if it has not left the warehouse.", "inbox"),
    ("E17", "Nora Lind", "nora.lind@example.com", "Mat smell", "Is a chemical smell normal on a new yoga mat?", "inbox"),
    ("E18", "Chris Hale", "chris.hale@example.com", "Old mug", "The mug I bought six weeks ago leaks. What can you do?", "inbox"),
]

INCIDENTS = [
    ("INC-14", "Checkout 500s after Friday deploy", "open", "degraded", "2026-09-19", "Shoppers see HTTP 500 on checkout after the Friday payment deploy."),
    ("INC-15", "Label printer jam", "open", "none", "2026-09-20", "Warehouse printer 2 jams on large labels. Orders still ship."),
    ("INC-16", "Search typos", "monitoring", "none", "2026-09-12", "Search misses a plural on 'tents'. A fix is in review."),
    ("INC-17", "Image CDN slow", "open", "degraded", "2026-09-18", "Product photos load slowly in the EU. Pages still work."),
    ("INC-18", "Email delay", "closed", "none", "2026-09-02", "Password reset mail was delayed for two hours. Recovered."),
    ("INC-19", "Inventory sync lag", "open", "degraded", "2026-09-21", "Wholesale stock counts lag by 20 minutes."),
    ("INC-20", "Payment webhook retries", "closed", "degraded", "2026-08-30", "Duplicate webhook retries. Stopped after a config change."),
    ("INC-21", "Mobile menu overlap", "closed", "none", "2026-08-11", "Cosmetic overlap on small screens."),
    ("INC-22", "Staging disk full", "open", "none", "2026-09-21", "Staging runner disk is full. Production is fine."),
    ("INC-23", "Tax lookup timeout", "monitoring", "degraded", "2026-09-15", "A few checkout tax calls time out, then succeed on retry."),
    ("INC-24", "Returns portal blank", "closed", "degraded", "2026-07-19", "Returns form was blank for an hour."),
    ("INC-25", "Gift card decimal", "closed", "none", "2026-06-02", "Gift cards rounded the wrong way. Patched."),
    ("INC-26", "Boulder store pickup", "open", "none", "2026-09-16", "Boulder pickup slot list is empty. Other stores are fine."),
    ("INC-27", "API rate limit", "monitoring", "degraded", "2026-09-11", "Partner API returned 429s for ten minutes."),
    ("INC-28", "Packaging recycle note", "closed", "none", "2026-05-20", "Wrong recycling text on the box insert. Copy fixed."),
]


def build() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    connection = sqlite3.connect(DB_PATH)
    connection.executescript(
        """
        CREATE TABLE customers (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT,
            segment TEXT,
            notes TEXT
        );
        CREATE TABLE products (
            sku TEXT PRIMARY KEY,
            name TEXT,
            category_path TEXT,
            description TEXT,
            price_usd REAL
        );
        CREATE TABLE orders (
            id TEXT PRIMARY KEY,
            customer_id TEXT,
            status TEXT,
            days_since_purchase INTEGER,
            total_usd REAL,
            charge_count INTEGER,
            created_on TEXT
        );
        CREATE TABLE order_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            sku TEXT,
            description TEXT,
            amount_usd REAL
        );
        CREATE TABLE support_tickets (
            id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_id TEXT,
            subject TEXT,
            body TEXT,
            channel TEXT,
            created_on TEXT
        );
        CREATE TABLE emails (
            id TEXT PRIMARY KEY,
            sender_name TEXT,
            sender_email TEXT,
            subject TEXT,
            body TEXT,
            folder TEXT
        );
        CREATE TABLE incidents (
            id TEXT PRIMARY KEY,
            title TEXT,
            status TEXT,
            customer_impact TEXT,
            opened_on TEXT,
            summary TEXT
        );
        """
    )
    connection.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)", CUSTOMERS)
    connection.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", PRODUCTS)
    connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)", ORDERS)
    connection.executemany(
        "INSERT INTO order_lines (order_id, sku, description, amount_usd) VALUES (?, ?, ?, ?)",
        ORDER_LINES,
    )
    connection.executemany("INSERT INTO support_tickets VALUES (?, ?, ?, ?, ?, ?, ?)", TICKETS)
    connection.executemany("INSERT INTO emails VALUES (?, ?, ?, ?, ?, ?)", EMAILS)
    connection.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?)", INCIDENTS)
    connection.commit()
    connection.close()
    print(f"wrote {DB_PATH}")


if __name__ == "__main__":
    build()
