from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Book Management API")

class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float

books = []

@app.get("/")
def home():
    return {"message": "Book Management API Running"}

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.post("/books")
def add_book(book: Book):
    for b in books:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books.append(book)
    return {"message": "Book added successfully"}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            books.pop(index)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")