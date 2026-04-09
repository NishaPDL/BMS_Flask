import requests
from models import Book
from config.config import db

def fetch_books(title, authors, isbn, publisher, num_pages, required_books):
    """Fetch books locally or from a custom source."""
    fetched_books = []
    
    # For now, I'll assume you simply want to query the local database
    query = Book.select().where(
        (Book.title.contains(title)) & 
        (Book.author.contains(authors)) & 
        (Book.isbn.contains(isbn)) & 
        (Book.publisher.contains(publisher)) & 
        (Book.num_pages >= num_pages)
    )

    # Add matching books to fetched_books until you reach the required_books count
    for book in query:
        fetched_books.append(book.__dict__)
        if len(fetched_books) >= required_books:
            break

    return fetched_books[:required_books]  # Return exactly required_books

def save_books_to_db(books):
    """Save fetched books into the local database, updating stock if the book already exists."""
    added_books = 0
    
    for book in books:
        title = book["title"]
        authors = book.get("authors", "Unknown")
        isbn = book.get("isbn", None)
        publisher = book.get("publisher", "N/A")
        num_pages = int(book.get("num_pages", 0))
        publication_date = int(book.get("publication_date", "2000").split("/")[-1])  # Extracting year
        language = book.get("language_code", "English")
        
        # Check if the book already exists based on ISBN
        existing_book = Book.get_or_none(Book.isbn == isbn)

        if existing_book:
            # Update stock count
            existing_book.stock += 1
            existing_book.save()
        else:
            # Create new book entry
            Book.create(
                title=title,
                author=authors,
                isbn=isbn,
                publisher=publisher,
                num_pages=num_pages,
                publication_date=publication_date,
                language=language,
                stock=1,  # Initial stock count
                mrp=0.0,  # Default value (you can update this)
                times_issued=0
            )
            added_books += 1
    
    return {"success": f"{added_books} new books added, existing books updated!"}

# Example usage:
# books_to_add = fetch_books("Python", "Guido", "", "O'Reilly", 300, 5)
# result = save_books_to_db(books_to_add)
# print(result)