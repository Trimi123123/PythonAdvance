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
    return {"message": "Country Population Manager API is running"}


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


@app.post("/countries")
def add_country(country: CountryCreate):
    name = normalize_name(country.name)
    conn = get_connection()
    cur = conn.cursor()
    try:
        # FIXED: Reduced exact placeholder match counts to 6 elements
        cur.execute("""
            INSERT INTO countries
            (name, population, capital, currency, continent, independence_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name, country.population, country.capital,
            country.currency, country.continent, country.independence_year
        ))
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.close()
        message = str(e).lower()
        if "name" in message:
            raise HTTPException(status_code=400, detail="Country already exists")
        raise HTTPException(status_code=400, detail="Database constraint error")
    conn.close()
    return {"message": f"{name} added successfully"}


@app.put("/countries/{country_name}")
def update_country(country_name: str, update: CountryUpdate):
    name = normalize_name(country_name)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM countries WHERE name = ?", (name,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Country not found")

    update_data = update.dict(exclude_unset=True)
    if not update_data:
        conn.close()
        return {"message": "No fields updated"}

    clauses = [f"{key} = ?" for key in update_data.keys()]
    values = list(update_data.values())
    values.append(name)

    sql = f"UPDATE countries SET {', '.join(clauses)} WHERE name = ?"
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return {"message": f"{name} updated successfully"}


@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    name = normalize_name(country_name)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries WHERE name = ?", (name,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Country not found")
    cur.execute("DELETE FROM countries WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return {"message": f"{name} deleted successfully"}