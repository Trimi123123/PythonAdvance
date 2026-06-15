from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Country Population Manager API")

# ---------------- DATA ----------------
countries: Dict[str, int] = {
    "Kosovo": 1800000,
    "Albania": 2800000,
    "Germany": 84000000,
    "USA": 331000000
}

# ---------------- MODEL ----------------
class Country(BaseModel):
    name: str
    population: int


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Country Population Manager API is running"}


# ---------------- GET COUNTRIES ----------------
@app.get("/countries")
def get_countries():
    return countries


# ---------------- STATS (FIXED) ----------------
@app.get("/stats")
def get_stats():
    values = list(countries.values())

    if len(values) == 0:
        return {
            "total_countries": 0,
            "max_population": 0,
            "min_population": 0,
            "average_population": 0
        }

    return {
        "total_countries": len(countries),
        "max_population": max(values),
        "min_population": min(values),
        "average_population": sum(values) // len(values)
    }


# ---------------- ADD ----------------
@app.post("/countries")
def add_country(country: Country):
    name = country.name.strip().title()

    if name in countries:
        raise HTTPException(status_code=400, detail="Country already exists")

    countries[name] = country.population
    return {"message": f"{name} added successfully"}


# ---------------- UPDATE ----------------
@app.put("/countries/{country_name}")
def update_country(country_name: str, population: int):
    name = country_name.strip().title()

    if name not in countries:
        raise HTTPException(status_code=404, detail="Country not found")

    countries[name] = population
    return {"message": f"{name} updated successfully"}


# ---------------- DELETE ----------------
@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    name = country_name.strip().title()

    if name not in countries:
        raise HTTPException(status_code=404, detail="Country not found")

    del countries[name]
    return {"message": f"{name} deleted successfully"}