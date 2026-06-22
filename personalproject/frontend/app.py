import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Country Intelligence Hub", layout="wide")
st.title("🌍 Country Intelligence Hub")


# ----------------- NETWORK WRAPPERS -----------------
def safe_request(method, endpoint, payload=None):
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET":
            res = requests.get(url, timeout=5)
        elif method == "POST":
            res = requests.post(url, json=payload, timeout=5)
        elif method == "PUT":
            res = requests.put(url, json=payload, timeout=5)
        elif method == "DELETE":
            res = requests.delete(url, timeout=5)
        return res, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


# ----------------- DATA LOADING -----------------
stats_res, stats_err = safe_request("GET", "/stats")
stats = stats_res.json() if (stats_res and stats_res.status_code == 200) else {
    "total_countries": 0, "max_population": 0, "min_population": 0, "average_population": 0, "total_population": 0
}

countries_res, countries_err = safe_request("GET", "/countries")
countries_list = countries_res.json() if (countries_res and countries_res.status_code == 200) else []

# ----------------- GLOBAL STATS KPI -----------------
st.subheader("📊 Network Summary")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Countries", stats.get("total_countries", 0))
c2.metric("Max Population", f"{stats.get('max_population', 0):,}")
c3.metric("Min Population", f"{stats.get('min_population', 0):,}")
c4.metric("Avg Population", f"{stats.get('average_population', 0):,}")
c5.metric("Global Population", f"{stats.get('total_population', 0):,}")
st.divider()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.header("🔍 Directory Filters")
search_query = st.sidebar.text_input("Search Country by Name").strip().lower()

continents = sorted(list({c['continent'] for c in countries_list if c.get('continent')}))
selected_continent = st.sidebar.selectbox("Filter by Continent", ["All"] + continents)

# Apply Filter Execution
filtered_countries = countries_list
if search_query:
    filtered_countries = [c for c in filtered_countries if search_query in c['name'].lower()]
if selected_continent != "All":
    filtered_countries = [c for c in filtered_countries if c.get('continent') == selected_continent]

# ----------------- MAIN INTERFACE TABS -----------------
tab_view, tab_add, tab_update, tab_delete = st.tabs([
    "📋 View Directory", "➕ Add Record", "✏️ Edit Record", "🗑️ Remove Record"
])

# --- TAB 1: VIEW RECORDS ---
with tab_view:
    st.subheader("Country Metadata Cards")
    if not filtered_countries:
        st.info("No records match your query filters.")
    else:
        for c in filtered_countries:
            with st.expander(f"📌 {c['name']} (Pop: {c['population']:,})"):
                col_left, col_right = st.columns(2)
                with col_left:
                    st.write(f"**Capital:** {c.get('capital') or 'N/A'}")
                    st.write(f"**Continent:** {c.get('continent') or 'N/A'}")
                with col_right:
                    st.write(f"**Currency:** {c.get('currency') or 'N/A'}")
                    st.write(f"**Independence Year:** {c.get('independence_year') or 'N/A'}")

# --- TAB 2: ADD RECORD ---
with tab_add:
    st.subheader("Insert New Country to Database")
    with st.form("add_form", clear_on_submit=True):
        a_name = st.text_input("Country Name *")
        a_pop = st.number_input("Population *", min_value=0, value=0, step=1000)

        col_a, col_b = st.columns(2)
        with col_a:
            a_cap = st.text_input("Capital")
            a_cont = st.text_input("Continent")
        with col_b:
            a_curr = st.text_input("Currency (e.g., USD, EUR)")
            a_ind = st.number_input("Independence Year", min_value=0, max_value=2026, value=0, step=1)

        submitted = st.form_submit_button("Commit Entry")
        if submitted:
            if not a_name.strip():
                st.error("Country Name is a mandatory field.")
            else:
                payload = {
                    "name": a_name,
                    "population": int(a_pop),
                    "capital": a_cap or None,
                    "currency": a_curr or None,
                    "continent": a_cont or None,
                    "independence_year": int(a_ind) if a_ind > 0 else None
                }
                res, err = safe_request("POST", "/countries", payload)
                if err:
                    st.error(f"Network error: {err}")
                elif res.status_code in [200, 201]:
                    st.success("Country added successfully!")
                    st.rerun()
                else:
                    try:
                        error_detail = res.json().get("detail", "Error adding country.")
                    except ValueError:
                        error_detail = f"Server Error {res.status_code}: {res.text or 'No response body'}"
                    st.error(error_detail)

# --- TAB 3: EDIT RECORD ---
with tab_update:
    st.subheader("Modify Existing Record Elements")
    country_names = [c["name"] for c in countries_list]

    if not country_names:
        st.info("No records available to mutate.")
    else:
        target_country = st.selectbox("Select Target Country to Update", country_names, key="update_select_box")
        current_data = next(item for item in countries_list if item["name"] == target_country)

        st.info(f"Modifying fields for **{target_country}**.")

        with st.form("update_form"):
            u_pop = st.number_input("New Population", min_value=0, value=int(current_data['population']), step=1000, key=f"u_pop_{target_country}")

            col_u1, col_u2 = st.columns(2)
            with col_u1:
                u_cap = st.text_input("Update Capital", value=current_data.get('capital') or "", key=f"u_cap_{target_country}")
                u_cont = st.text_input("Update Continent", value=current_data.get('continent') or "", key=f"u_cont_{target_country}")
            with col_u2:
                u_curr = st.text_input("Update Currency", value=current_data.get('currency') or "", key=f"u_curr_{target_country}")
                u_ind = st.number_input("Update Independence Year", min_value=0, max_value=2026, value=int(current_data.get('independence_year') or 0), step=1, key=f"u_ind_{target_country}")

            update_submitted = st.form_submit_button("Push Update Payload")
            if update_submitted:
                payload = {
                    "population": int(u_pop),
                    "capital": u_cap or None,
                    "currency": u_curr or None,
                    "continent": u_cont or None,
                    "independence_year": int(u_ind) if u_ind > 0 else None
                }
                res, err = safe_request("PUT", f"/countries/{target_country}", payload)
                if err:
                    st.error(f"Network error: {err}")
                elif res.status_code == 200:
                    st.success("Country updated successfully!")
                    st.rerun()
                else:
                    try:
                        error_detail = res.json().get("detail", "Error updating country.")
                    except ValueError:
                        error_detail = f"Server Error {res.status_code}: {res.text or 'No response body'}"
                    st.error(error_detail)

# --- TAB 4: REMOVE RECORD ---
with tab_delete:
    st.subheader("Drop Country From System")
    country_names = [c["name"] for c in countries_list]

    if not country_names:
        st.info("No records left to remove.")
    else:
        drop_target = st.selectbox("Select Target Country to Purge", country_names, key="delete_box")
        st.warning(f"Warning: This action completely removes **{drop_target}** from the persistent database context.")

        confirm_check = st.checkbox(f"I confirm I want to drop {drop_target}", key=f"confirm_{drop_target}")

        if st.button("Execute Drop Sequence"):
            if confirm_check:
                res, err = safe_request("DELETE", f"/countries/{drop_target}")
                if err:
                    st.error(f"Network error: {err}")
                elif res.status_code == 200:
                    st.success("Country deleted successfully!")
                    st.rerun()
                else:
                    try:
                        error_detail = res.json().get("detail", "Error deleting country.")
                    except ValueError:
                        error_detail = f"Server Error {res.status_code}: {res.text or 'No response body'}"
                    st.error(error_detail)
            else:
                st.error("Please assert safety confirmation checks prior to clearing records.")