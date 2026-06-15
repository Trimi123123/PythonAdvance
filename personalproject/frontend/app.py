import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Country Population Manager", layout="wide")

st.title("🌍 Country Population Manager")
st.caption("A simple full-stack CRUD dashboard using FastAPI + Streamlit")

# ---------------- SAFE STATS ----------------
stats_response = requests.get(f"{API_URL}/stats")

if stats_response.status_code == 200:
    stats = stats_response.json()
else:
    stats = {
        "total_countries": 0,
        "max_population": 0,
        "min_population": 0,
        "average_population": 0
    }

# ---------------- STATS UI ----------------
st.subheader("📊 Global Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Countries", stats.get("total_countries", 0))
col2.metric("Max Population", stats.get("max_population", 0))
col3.metric("Min Population", stats.get("min_population", 0))
col4.metric("Average Population", stats.get("average_population", 0))

st.divider()

# ---------------- COUNTRIES ----------------
st.subheader("🌐 Countries List")

data = requests.get(f"{API_URL}/countries").json()

for country, pop in data.items():
    st.write(f"**{country}** → {pop:,}")

st.divider()

# ---------------- ADD ----------------
st.subheader("➕ Add Country")

name = st.text_input("Country Name")
population = st.number_input("Population", min_value=0, step=1000)

if st.button("Add Country"):
    if name:
        requests.post(
            f"{API_URL}/countries",
            json={"name": name, "population": int(population)}
        )
        st.success("Country added")
        st.rerun()

st.divider()

# ---------------- UPDATE ----------------
st.subheader("✏️ Update Country")

u_name = st.text_input("Country to Update")
u_pop = st.number_input("New Population", min_value=0, step=1000, key="update")

if st.button("Update Country"):
    requests.put(
        f"{API_URL}/countries/{u_name}",
        params={"population": int(u_pop)}
    )
    st.success("Updated")
    st.rerun()

st.divider()

# ---------------- DELETE ----------------
st.subheader("🗑️ Delete Country")

d_name = st.text_input("Country to Delete")

if st.button("Delete Country"):
    requests.delete(f"{API_URL}/countries/{d_name}")
    st.warning("Deleted")
    st.rerun()