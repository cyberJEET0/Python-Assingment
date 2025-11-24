import logging
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

logging.basicConfig(level=logging.INFO, filename="library.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def menu():
    inventory = LibraryInventory()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                book = Book(title, author, isbn)
                inventory.add_book(book)

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book:
                    book.issue()
                    inventory.save_books()
                else:
                    print("Book not found.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book:
                    book.return_book()
                    inventory.save_books()
                else:
                    print("Book not found.")

            elif choice == "4":
                for b in inventory.display_all():
                    print(b)

            elif choice == "5":
                title = input("Enter title keyword: ")
                results = inventory.search_by_title(title)
                for b in results:
                    print(b)

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            logging.error(f"Error in menu: {e}")

if __name__ == "__main__":
    menu()
