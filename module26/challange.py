import streamlit as st
import pandas as pd
import sqlite3

# =========================
# DATABASE CONNECTION
# =========================
conn = sqlite3.connect("recipes.db", check_same_thread=False)
cursor = conn.cursor()

# =========================
# CREATE TABLES
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    cooking_time INTEGER NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
""")

conn.commit()

# =========================
# APP TITLE
# =========================
st.title("Online Recipe Book")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["View Recipes", "Add Recipe", "Add Category"]
)

# =========================
# VIEW RECIPES
# =========================
if menu == "View Recipes":

    st.header("Recipes")

    query = """
    SELECT
        recipes.name AS Recipe,
        recipes.ingredients AS Ingredients,
        recipes.cooking_time AS Cooking_Time,
        categories.name AS Category
    FROM recipes
    LEFT JOIN categories
    ON recipes.category_id = categories.id
    """

    df = pd.read_sql_query(query, conn)

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No recipes available")

# =========================
# ADD CATEGORY
# =========================
elif menu == "Add Category":

    st.header("Add Category")

    category = st.text_input("Category Name")

    if st.button("Add Category"):

        if category.strip() == "":
            st.warning("Please enter a category name")

        else:
            cursor.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (category,)
            )

            conn.commit()

            st.success("Category added successfully")

# =========================
# ADD RECIPE
# =========================
elif menu == "Add Recipe":

    st.header("Add Recipe")

    name = st.text_input("Recipe Name")

    ingredients = st.text_area("Ingredients")

    cooking_time = st.number_input(
        "Cooking Time (minutes)",
        min_value=1,
        step=1
    )

    # GET CATEGORIES FROM DATABASE
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if categories:

        category_names = [category[1] for category in categories]

        selected_category = st.selectbox(
            "Select Category",
            category_names
        )

        if st.button("Add Recipe"):

            if name.strip() == "" or ingredients.strip() == "":
                st.warning("Please fill all fields")

            else:

                # FIND CATEGORY ID
                category_id = None

                for category in categories:
                    if category[1] == selected_category:
                        category_id = category[0]

                # INSERT RECIPE
                cursor.execute("""
                INSERT INTO recipes
                (name, ingredients, cooking_time, category_id)
                VALUES (?, ?, ?, ?)
                """, (
                    name,
                    ingredients,
                    cooking_time,
                    category_id
                ))

                conn.commit()

                st.success("Recipe added successfully")

    else:
        st.warning("Please add a category first")

