import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_books):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(num_books):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        db.execute('INSERT INTO contacts (title, genre) VALUES (?, ?)', (title, genre))
    db.commit()
    print(f'{num_books} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.
