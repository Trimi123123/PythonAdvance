import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📚 Book Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["View Books", "Add Book", "Search Book", "Delete Book"]
)

if menu == "View Books":
    st.header("All Books")

    response = requests.get(f"{API_URL}/books")

    if response.status_code == 200:
        books = response.json()

        if books:
            st.table(books)
        else:
            st.info("No books available")

elif menu == "Add Book":
    st.header("Add New Book")

    book_id = st.number_input("Book ID", min_value=1, step=1)
    title = st.text_input("Title")
    author = st.text_input("Author")
    price = st.number_input("Price", min_value=0.0)

    if st.button("Add"):
        payload = {
            "id": int(book_id),
            "title": title,
            "author": author,
            "price": price
        }

        response = requests.post(
            f"{API_URL}/books",
            json=payload
        )

        if response.status_code == 200:
            st.success("Book Added")
        else:
            st.error(response.json()["detail"])

elif menu == "Search Book":
    st.header("Search Book")

    book_id = st.number_input(
        "Enter Book ID",
        min_value=1,
        step=1
    )

    if st.button("Search"):
        response = requests.get(
            f"{API_URL}/books/{int(book_id)}"
        )

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Book Not Found")

elif menu == "Delete Book":
    st.header("Delete Book")

    book_id = st.number_input(
        "Book ID",
        min_value=1,
        step=1
    )

    if st.button("Delete"):
        response = requests.delete(
            f"{API_URL}/books/{int(book_id)}"
        )

        if response.status_code == 200:
            st.success("Book Deleted")
        else:
            st.error("Book Not Found")