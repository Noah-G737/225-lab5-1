from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            book_id = request.form.get('book_id')
            db = get_db()
            db.execute('DELETE FROM Books WHERE id = ?', (book_id,))
            db.commit()
            message = 'Book deleted successfully.'
        else:
            title = request.form.get('title')
            genre = request.form.get('genre')
            if title and genre:
                db = get_db()
                db.execute('INSERT INTO  (title, genre) VALUES (?, ?)', (title, genre))
                db.commit()
                message = 'Book added successfully.'
            else:
                message = 'Missing title or genre.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM Books').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contacts</title>
        </head>
        <body>
            <h2>Add Contacts</h2>
            <form method="POST" action="/">
                <label for="">title:</label><br>
                <input type="text" id="title" name="title" required><br>
                <label for="genre">genre:</label><br>
                <input type="text" id="genre" name="genre" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if contacts %}
                <table border="1">
                    <tr>
                        <th>Title</th>
                        <th>Genre</th>
                        <th>Delete</th>
                    </tr>
                    {% for book in books %}
                        <tr>
                            <td>{{ book['title'] }}</td>
                            <td>{{ book['title'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="book_id" value="{{ book['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
