import sqlite3

class Country:
    def __init__(self, id, name, population, capital, currency, continent, independence_year):
        self.id = id
        self.name = name
        self.population = population
        self.capital = capital
        self.currency = currency
        self.continent = continent
        self.independence_year = independence_year

    @classmethod
    def from_row(cls, row):

        if not row:
            return None
        return cls(*row)

def create_tables(db_name="countries.db"):

    with sqlite3.connect(db_name) as conn:
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
        );
        """)
        conn.commit()