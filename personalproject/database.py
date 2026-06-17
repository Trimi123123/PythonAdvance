import sqlite3

conn = sqlite3.connect("countries.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    population INTEGER NOT NULL,
    capital TEXT,
    region TEXT,
    area_km2 REAL,
    gdp_usd REAL,
    currency TEXT,
    iso_code TEXT UNIQUE,
    continent TEXT,
    independence_year INTEGER
)
""")

# Optional starter data
starter_data = [
    ("Kosovo", 1800000, "Pristina", "Balkans", 10887, 10300000000, "EUR", "XKX", "Europe", 2008),
    ("Albania", 2800000, "Tirana", "Balkans", 28748, 23000000000, "ALL", "ALB", "Europe", 1912),
    ("Germany", 84000000, "Berlin", "Western Europe", 357588, 4500000000000, "EUR", "DEU", "Europe", 1871),
    ("USA", 331000000, "Washington, D.C.", "North America", 9834000, 28000000000000, "USD", "USA", "North America", 1776),
]

for row in starter_data:
    cur.execute("""
    INSERT OR IGNORE INTO countries
    (name, population, capital, region, area_km2, gdp_usd, currency, iso_code, continent, independence_year)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()
conn.close()
