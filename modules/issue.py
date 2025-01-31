from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)


issue_bp = Blueprint('issue', __name__)  # Define a blueprint for issue book-related routes

@issue_bp.route('/issue_page')
def issue_page():
    return render_template('issue_book.html')


# Route to handle both the "Submit" and "Show" button actions
@issue_bp.route('/submit_or_show_or_back', methods=['POST'])
def submit_or_show():
    try:
        action = request.form.get('action')  # Get the action type from hidden input
        book_name = request.form.get('book')  # Get book name from form

        if action == 'submit':
        # Process the book issue logic
            roll_no = request.form['roll_no']
            username = request.form['username']
            author_name = request.form['author']
            pub_name = request.form['publisher']
            date_of_issue = request.form['date_of_issue']

            conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
            cursor = conn.cursor()

            # Check if the student already has 3 books issued or if this book has been issued before
            cursor.execute("SELECT * FROM student_lib WHERE roll_no=?", (roll_no,))
            issued_books = cursor.fetchall()

            cursor.execute("SELECT * FROM student_lib WHERE roll_no=? AND name=? AND book_name=?", (roll_no, username, book_name))
            existing_issue = cursor.fetchall()

            cursor.execute("SELECT * FROM student_id WHERE name=?", (username,))
            student_exists = cursor.fetchall()

            cursor.execute("SELECT * FROM books_lib WHERE NAME_BOOK=?", (book_name,))
            book_exists = cursor.fetchall()

            cursor.execute("SELECT * FROM student_id WHERE roll_no=? AND name=?", (roll_no, username))
            check_username_roll_no = cursor.fetchone()  # Fetch single matching record if it exists

            if student_exists and book_exists:
                count = len(issued_books)
                if check_username_roll_no:  # Check if roll_no and username pair exists
                    if count < 3 and not existing_issue:
                        # Insert new issue entry
                        cursor.execute(
                            "INSERT INTO student_lib (roll_no, name, book_name, author, publ, doi, dor) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (roll_no, username, book_name, author_name, pub_name, date_of_issue, date_of_issue))
                        conn.commit()

                        cursor.execute("update student_lib set dor=date(doi,'+15 days')" )
                        conn.commit()

                        flash("ISSUE SUCCESSFUL", "success")

                    elif existing_issue:
                        flash("BOOK ALREADY ISSUED!!!", "error")
                    
                    elif count == 3:
                        flash("ISSUE FAILED: Maximum limit reached.", "error")
                    
                    else:
                        flash("THIS BOOK CAN'T BE ISSUED", "error")
                
                else:
                    flash("ROLL NUMBER AND USERNAME DO NOT MATCH", "error")  # Added clear error message for mismatch
            
            elif not student_exists:
                flash("USERNAME NOT PRESENT", "error")
            elif not book_exists:
                flash("BOOK NOT PRESENT!!!", "error")

            conn.close()
            return render_template('issue_book.html')
        
        elif action == 'show':
            roll_no = request.form['roll_no']
            username = request.form['username']
        
        
        # Fetch and display author and publisher details for the given book
            conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
            cursor = conn.cursor()

            cursor.execute("SELECT AUTHOR_BOOK, PUB_BOOK FROM books_lib WHERE NAME_BOOK=?", (book_name,))
            book_details = cursor.fetchone()
            conn.close()

            if book_details:
                flash("BOOK FOUND!!!", "success")
                author, publisher = book_details
                return render_template('issue_book.html', book_name=book_name, author_name=author, pub_name=publisher, roll_no=roll_no, username=username)
            
            else:
                flash("BOOK NOT FOUND!!!", "error")
                return render_template('issue_book.html')
            
        elif action=='BACK':
            return render_template('menu_page.html')
        

    except Exception as e:
        logging.error(f'Error occurred: {e}')
        flash("An error occurred.", "error")
    
