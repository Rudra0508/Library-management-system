from flask import Blueprint, render_template, request
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

# Define the blueprint
display_book_bp = Blueprint('display_books', __name__)

@display_book_bp.route('/display_books_page')
def show_books_page():
    return render_template('display_all_books.html', books=None)

@display_book_bp.route('/display_all_books', methods=['POST'])
def display_all_books():
    try:
        # Connect to the database
        conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
        cursor = conn.cursor()

        # Fetch all books from the database
        cursor.execute("SELECT * FROM books_lib")
        books = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Pass the data to the template
        return render_template('display_all_books.html', books=books)

    except Exception as e:
        logging.error(f"Error fetching books: {e}")
        return f"An error occurred: {e}"
