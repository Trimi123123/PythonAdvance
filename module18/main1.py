import streamlit as st
import pandas as pd
import plotly.express as px

books_df = pd.read_csv("bestsellers_with_categories_2022_03_27.csv")

st.title("Bestselling Books")
st.write("This app analyzes the Amazon top selling books")

st.subheader("Summary Statistic")
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Total Books", value=total_books)
col2.metric(label="Unique Titles", value=unique_titles)
col3.metric(label="Average Rating", value=average_rating)
col4.metric(label="Average Price", value=average_price)

st.subheader("Dataset Preview")
st.write(books_df.head())

with col1:
    st.subheader("Top 10 book Titles")
    top_titles = books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 Book Authors")
    top_authors = books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)