import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_books():
    """Clear only the test books from the database."""
    db = connect_db()
    # Assuming all test contacts follow a specific naming pattern
    db.execute("DELETE FROM books WHERE title LIKE 'Test Title %'")
    db.commit()
    print('Test books have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_books()
