import sqlite3

conn = sqlite3.connect("countries.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    population INTEGER NOT NULL,
    capital TEXT,
    currency TEXT,
    continent TEXT,
    independence_year INTEGER
)
""")


starter_data = [
    ("Kosovo", 1800000, "Pristina", "EUR", "XKX", "Europe", 2008),
    ("Albania", 2800000, "Tirana", "ALL", "ALB", "Europe", 1912),
    ("Germany", 84000000, "Berlin", "EUR", "DEU", "Europe", 1871),
    ("USA", 331000000, "Washington, D.C.","USD", "USA", "North America", 1776),
]

for row in starter_data:
    cur.execute("""
    INSERT OR IGNORE INTO countries
    (name, population, capital, currency, continent, independence_year)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()
conn.close()
