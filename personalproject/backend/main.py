from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3

app = FastAPI(title="Country Population Manager API")
DB_NAME = "countries.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------- DB AUTO-INITIALIZATION -----------------
def init_db():
    """Creates the database file and countries table automatically if missing."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT PRIMARY KEY,
            population INTEGER NOT NULL,
            capital TEXT,
            currency TEXT,
            continent TEXT,
            independence_year INTEGER
        )
    """)
    conn.commit()

    # Optional: Seed data if database is empty
    cur.execute("SELECT COUNT(*) FROM countries")
    if cur.fetchone()[0] == 0:
        sample_countries = [
            ("United States", 333000000, "Washington D.C.", "USD", "North America", 1776),
            ("Germany", 83000000, "Berlin", "EUR", "Europe", 1871),
            ("Japan", 125000000, "Tokyo", "JPY", "Asia", None)
        ]
        cur.executemany("""
            INSERT INTO countries (name, population, capital, currency, continent, independence_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_countries)
        conn.commit()
        print("Database seeded with sample records successfully.")

    conn.close()


# Run table initialization instantly during file startup
init_db()


def normalize_name(name: str) -> str:
    return name.strip().title()


class CountryCreate(BaseModel):
    name: str = Field(..., min_length=1)
    population: int = Field(..., ge=0)
    capital: Optional[str] = None
    currency: Optional[str] = None
    continent: Optional[str] = None
    independence_year: Optional[int] = None


class CountryUpdate(BaseModel):
    population: Optional[int] = Field(None, ge=0)
    capital: Optional[str] = None
    currency: Optional[str] = None
    continent: Optional[str] = None
    independence_year: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Country Population Manager API is running and healthy"}


@app.get("/countries")
def get_countries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/stats")
def get_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            COUNT(*) as total_countries,
            COALESCE(MAX(population), 0) as max_population,
            COALESCE(MIN(population), 0) as min_population,
            COALESCE(AVG(population), 0) as average_population,
            COALESCE(SUM(population), 0) as total_population
        FROM countries
    """)
    row = cur.fetchone()
    conn.close()
    return {
        "total_countries": row["total_countries"],
        "max_population": row["max_population"],
        "min_population": row["min_population"],
        "average_population": int(row["average_population"]),
        "total_population": row["total_population"],
    }


@app.post("/countries", status_code=201)
def add_country(country: CountryCreate):
    normalized_name = normalize_name(country.name)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM countries WHERE name = ?", (normalized_name,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(
            status_code=400, detail=f"Country '{normalized_name}' already exists."
        )

    try:
        cur.execute(
            """
            INSERT INTO countries (name, population, capital, currency, continent, independence_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                normalized_name,
                country.population,
                country.capital,
                country.currency,
                country.continent,
                country.independence_year,
            ),
        )
        conn.commit()

        cur.execute("SELECT * FROM countries WHERE name = ?", (normalized_name,))
        new_country = dict(cur.fetchone())
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {str(e)}"
        )

    conn.close()
    return new_country


@app.get("/countries/{name}")
def get_country_by_name(name: str):
    normalized_name = normalize_name(name)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM countries WHERE name = ?", (normalized_name,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=404, detail=f"Country '{normalized_name}' not found."
        )

    return dict(row)


@app.put("/countries/{name}")
def update_country(name: str, country_data: CountryUpdate):
    normalized_name = normalize_name(name)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM countries WHERE name = ?", (normalized_name,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(
            status_code=404, detail=f"Country '{normalized_name}' not found."
        )

    update_data = country_data.dict(exclude_unset=True)
    if not update_data:
        conn.close()
        return dict(row)

    fields = ", ".join([f"{key} = ?" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(normalized_name)

    try:
        cur.execute(
            f"UPDATE countries SET {fields} WHERE name = ?", tuple(values)
        )
        conn.commit()

        cur.execute("SELECT * FROM countries WHERE name = ?", (normalized_name,))
        updated_country = dict(cur.fetchone())
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {str(e)}"
        )

    conn.close()
    return updated_country


@app.delete("/countries/{name}")
def delete_country(name: str):
    normalized_name = normalize_name(name)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM countries WHERE name = ?", (normalized_name,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(
            status_code=404, detail=f"Country '{normalized_name}' not found."
        )

    try:
        cur.execute("DELETE FROM countries WHERE name = ?", (normalized_name,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {str(e)}"
        )

    conn.close()
    return {"message": f"Country '{normalized_name}' successfully deleted."}
