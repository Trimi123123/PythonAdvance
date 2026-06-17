# models.py
import sqlite3

class Country:
    def __init__(self, id, name, population, capital, region, area_km2, gdp_usd, currency, iso_code, continent, independence_year):
        self.id = id
        self.name = name
        self.population = population
        self.capital = capital
        self.region = region
        self.area_km2 = area_km2
        self.gdp_usd = gdp_usd
        self.currency = currency
        self.iso_code = iso_code
        self.continent = continent
        self.independence_year = independence_year

    @classmethod
    def from_row(cls, row):

        if not row:
            return None
        return cls(*row)

    def __repr__(self):
        return f"<Country name='{self.name}' iso='{self.iso_code}'>"


def create_tables(db_name="countries.db"):

    with sqlite3.connect(db_name) as conn:
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