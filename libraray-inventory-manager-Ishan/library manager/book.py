import logging

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            logging.info(f"Book issued: {self.title}")
        else:
            logging.error(f"Book already issued: {self.title}")

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            logging.info(f"Book returned: {self.title}")
        else:
            logging.error(f"Book not issued: {self.title}")

    def is_available(self):
        return self.status == "available"
