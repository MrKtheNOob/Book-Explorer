
from db import DatabaseManager


dbm = DatabaseManager("./myfirstproject-9301a-firebase-adminsdk-fbsvc-b7b2ce8e2d.json")
def search_books(title: str):
    if not title:
       return "Title is required"
    books = dbm.list_books()
    filtered_books=[book for book in books if title.lower() in book.get("title","").lower()]    
    return filtered_books

print(search_books("silence"))