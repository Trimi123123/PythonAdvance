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

conn.commit()
conn.close()