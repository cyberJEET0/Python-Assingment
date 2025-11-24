import json
import logging
from pathlib import Path
from .book import Book

class LibraryInventory:
    def __init__(self, filename="catalog.json"):
        self.books = []
        self.filename = Path(filename)
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_isbn(self, isbn):
        return next((book for book in self.books if book.isbn == isbn), None)

    def display_all(self):
        return [str(book) for book in self.books]

    def save_books(self):
        try:
            with open(self.filename, "w") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error saving books: {e}")

    def load_books(self):
        try:
            if self.filename.exists():
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.books = [Book(**book) for book in data]
        except Exception as e:
            logging.error(f"Error loading books: {e}")
