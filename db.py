import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, List, Optional

class DatabaseManager:
    def __init__(self, cred_path: str, collection_name: str = "books") -> None:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.collection = self.db.collection(collection_name)

    def add_book(self, book: Dict[str, Any]) -> str:
        doc_ref = self.collection.document()
        doc_ref.set(book)
        return doc_ref.id

    def get_book(self, doc_id: str) -> Optional[Dict[str, Any]]:
        doc = self.collection.document(doc_id).get()
        return doc.to_dict() if doc.exists else None

    def update_book(self, doc_id: str, updates: Dict[str, Any]) -> None:
        doc_ref = self.collection.document(doc_id)
        doc_ref.update(updates)

    def delete_book(self, doc_id: str) -> None:
        self.collection.document(doc_id).delete()

    def list_books(self) -> List[Dict[str, Any]]:
        return [doc.to_dict() for doc in self.collection.stream()]

# Usage example (not in file)
# dbm = DatabaseManager("./myfirstproject-9301a-firebase-adminsdk-fbsvc-b7b2ce8e2d.json")
# book_id = dbm.add_book({"title": "Test", "authors": ["Author"], "publishedDate": "2025", "imageLink": "url"})
# book = dbm.get_book(book_id)
# dbm.update_book(book_id, {"title": "Updated Title"})
# dbm.delete_book(book_id)
# books = dbm.list_books()