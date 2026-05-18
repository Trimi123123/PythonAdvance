import streamlit as st
import pandas as pd

st.title("Online Recipe Book")

if "categories" not in st.session_state:
    st.session_state.categories = []

if "recipes" not in st.session_state:
    st.session_state.recipes = []

menu = st.sidebar.selectbox(
    "Menu",
    ["View Recipes", "Add Recipe", "Add Category"]
)

if menu == "View Recipes":

    st.header("Recipes")

    if st.session_state.recipes:
        df = pd.DataFrame(st.session_state.recipes)
        st.dataframe(df)
    else:
        st.info("No recipes available")


elif menu == "Add Category":

    st.header("Add Category")

    category = st.text_input("Category Name")

    if st.button("Add Category"):

        st.session_state.categories.append(category)

        st.success("Category added successfully")


elif menu == "Add Recipe":

    st.header("Add Recipe")

    name = st.text_input("Recipe Name")

    ingredients = st.text_area("Ingredients")

    cooking_time = st.number_input(
        "Cooking Time (minutes)",
        min_value=1
    )

    if st.session_state.categories:

        category = st.selectbox(
            "Select Category",
            st.session_state.categories
        )

        if st.button("Add Recipe"):

            st.session_state.recipes.append({
                "name": name,
                "ingredients": ingredients,
                "cooking_time": cooking_time,
                "category": category
            })

            st.success("Recipe added successfully")

    else:
        st.warning("Please add a category first")


