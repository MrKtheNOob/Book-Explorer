from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from db import DatabaseManager
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
dbm = DatabaseManager("./privatekey.json")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/books/all", response_class=HTMLResponse)
async def get_all_books(request: Request):
    books = dbm.list_books()
    return templates.TemplateResponse(
        "index.html", {"request": request, "books": books}
    )
    
# @app.get("/api/books/{book_id}")
# async def get_book(book_id: str):
#     book = dbm.get_book(book_id)
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book

@app.get("/api/books/search",response_class=HTMLResponse)
#take the name of the book as a path parameter for the search query 
async def search_books(request: Request, title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Title query parameter is required")
    books = dbm.list_books()
    filtered_books=[book for book in books if title.lower() in book.get("title","").lower()]    
    return templates.TemplateResponse(
        "books.html", {"request": request, "books": filtered_books}
    )
@app.post("/api/books")
async def create_book(book: dict):
    new_book = dbm.create_book(book)
    return new_book


@app.put("/api/books/{book_id}")
async def update_book(book_id: str, book: dict):
    updated_book = dbm.update_book(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@app.delete("/api/books/{book_id}")
async def delete_book(book_id: str):
    result = dbm.delete_book(book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
