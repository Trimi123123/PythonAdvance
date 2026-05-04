import streamlit as st
import requests
import pandas as pd

st.title("Project Management")

st.header("Add Developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input(
    "Experience Years: ",
    min_value=0,
    max_value=50,
    value=0
)

if st.button("Create Developer"):
    dev_data = {
        "name": dev_name,
        "experience": dev_experience
    }
    response = requests.post(
        url="http://127.0.0.1:8000/developer",
        json=dev_data
    )