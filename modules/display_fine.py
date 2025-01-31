from flask import Blueprint, render_template, request, session
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

display_fine_bp = Blueprint('display_fine', __name__)

@display_fine_bp.route('/display_fine_page')
def display_fine_page():
    # Check if the user is logged in
    if 'username' not in session:
        return "You must log in first!", 401  # Unauthorized access message
    
    return render_template('display_fine.html')


@display_fine_bp.route('/display_fine_code', methods=['POST'])
def display_fine_code():
    try:
        # Ensure the user is logged in
        if 'username' not in session or 'role' not in session:
            return "Unauthorized access. Please log in first.", 401
        
        # Connect to the SQLite database
        conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
        cursor = conn.cursor()

        # Fetch all book records
        role = session['role']
        username = session['username']

        if role == 'admin':
            # Admin sees all books
            cursor.execute("SELECT * FROM student_lib")
            fine_records = cursor.fetchall()
        else:
            # Students see only their own books (filtered by username)
            cursor.execute("SELECT * FROM student_lib WHERE name=?", (username,))
            fine_records = cursor.fetchall()

        combined_data = []  # To store combined data of records and fines

        # Calculate fines for each record
        for record in fine_records:
            date_of_issue = record[5]  # Index 5 corresponds to `date_of_issue`

            # Fetch today's date
            cursor.execute("SELECT DATE('now')")
            todays_date = cursor.fetchone()[0]

            # Calculate days issued
            cursor.execute("SELECT JULIANDAY(?) - JULIANDAY(?)", (todays_date, date_of_issue))
            days_issued = cursor.fetchone()[0]

            # Calculate fine if overdue
            if days_issued > 30:
                calculated_fine = int((days_issued - 30) * 2)  # Fine is 2 rupees per day overdue
            else:
                calculated_fine = 0  # No fine if within 30 days

            # Combine record and fine into one tuple
            combined_data.append(record + (calculated_fine,))

        conn.close()

        # Render the template with combined data
        return render_template('display_fine.html', combined_data=combined_data)

    except Exception as e:
        logging.error(f"Error fetching books: {e}")
        return f"An error occurred: {e}"
