import streamlit as st
import pandas as pd
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel



api = FastAPI()



conn = sqlite3.connect("recipes.db", check_same_thread=False)
cursor = conn.cursor()

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



class Category(BaseModel):
    name: str


class Recipe(BaseModel):
    name: str
    ingredients: str
    cooking_time: int
    category_id: int


@api.get("/categories")
def get_categories():
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1]
        })

    return result


@api.post("/categories")
def add_category(category: Category):
    cursor.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (category.name,)
    )
    conn.commit()
    return {"message": "Category added successfully"}


@api.get("/recipes")
def get_recipes():
    query = """
    SELECT
        recipes.name,
        recipes.ingredients,
        recipes.cooking_time,
        categories.name
    FROM recipes
    LEFT JOIN categories
    ON recipes.category_id = categories.id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "Recipe": row[0],
            "Ingredients": row[1],
            "Cooking Time": row[2],
            "Category": row[3]
        })

    return result


@api.post("/recipes")
def add_recipe(recipe: Recipe):
    cursor.execute("""
    INSERT INTO recipes
    (name, ingredients, cooking_time, category_id)
    VALUES (?, ?, ?, ?)
    """, (
        recipe.name,
        recipe.ingredients,
        recipe.cooking_time,
        recipe.category_id
    ))

    conn.commit()

    return {"message": "Recipe added successfully"}


st.title("Online Recipe Book")

menu_choice = st.sidebar.selectbox(
    "Menu",
    ["View Recipes", "Add Recipe", "Add Category"]
)


if menu_choice == "View Recipes":

    st.header("Recipes")

    recipes_data = get_recipes()

    if recipes_data:
        df = pd.DataFrame(recipes_data)
        st.dataframe(df)
    else:
        st.info("No recipes available")


elif menu_choice == "Add Category":

    st.header("Add Category")

    category_name_input = st.text_input("Category Name")

    if st.button("Add Category"):

        if category_name_input.strip() == "":
            st.warning("Please enter a category name")

        else:
            new_category = Category(name=category_name_input)
            add_category(new_category)
            st.success("Category added successfully")



elif menu_choice == "Add Recipe":

    st.header("Add Recipe")

    recipe_name_input = st.text_input("Recipe Name")
    ingredients_input = st.text_area("Ingredients")

    cooking_time_input = st.number_input(
        "Cooking Time (minutes)",
        min_value=1,
        step=1
    )

    categories_data = get_categories()

    if categories_data:

        category_names_list = []
        for cat_item in categories_data:
            category_names_list.append(cat_item["name"])

        selected_category_name = st.selectbox(
            "Select Category",
            category_names_list
        )

        if st.button("Add Recipe"):

            if recipe_name_input.strip() == "" or ingredients_input.strip() == "":
                st.warning("Please fill all fields")

            else:

                selected_category_id = None

                for cat_item in categories_data:
                    if cat_item["name"] == selected_category_name:
                        selected_category_id = cat_item["id"]

                new_recipe = Recipe(
                    name=recipe_name_input,
                    ingredients=ingredients_input,
                    cooking_time=int(cooking_time_input),
                    category_id=selected_category_id
                )

                add_recipe(new_recipe)

                st.success("Recipe added successfully")

    else:
        st.warning("Please add a category first")