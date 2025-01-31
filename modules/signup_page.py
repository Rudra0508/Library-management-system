from flask import Blueprint, render_template, redirect, request, flash, session, url_for
import sqlite3

# Create a Blueprint for the signup functionality
signup_bp = Blueprint('signup', __name__, template_folder='templates')

@signup_bp.route('/signup_page')
def signup_page():
    """Render the signup form."""
    return render_template('signup_page.html')

@signup_bp.route('/submit', methods=['POST'])
def signup_form():
    action = request.form.get('action')

    # Handle the BACK button
    if action == 'BACK':
        return render_template("login_page.html")

    # Handle the SUBMIT button
    if action == 'submit':
        roll_no = request.form['roll_no']
        username = request.form['username']
        email_id = request.form['email_id']
        address = request.form['address']
        class1 = request.form['class']
        password = request.form['password']
        confirm_pass = request.form['confirm_password']

        # Connect to the SQLite database
        db_path = r"C:\Users\admin\Desktop\app\db1.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check for existing username and roll number
        cursor.execute("SELECT * FROM student_id WHERE name=?", (username,))
        rs1 = cursor.fetchall()

        cursor.execute("SELECT * FROM student_id WHERE roll_no=?", (roll_no,))
        rs2 = cursor.fetchall()

        # Validate form and insert data
        if password == confirm_pass and not rs1 and not rs2:
            cursor.execute(
                """
                INSERT INTO student_id (roll_no, name, email_id, address, class, password)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (roll_no, username, email_id, address, class1, password)
            )
            conn.commit()
            flash("Signup successful!", "success")
            conn.close()
            return redirect(url_for('login.form'))  # Redirect to login page after successful signup
        elif password != confirm_pass:
            flash("Passwords do not match!", "error")
        elif rs1:
            flash("Username already exists!", "error")
        elif rs2:
            flash("Roll number already exists!", "error")

        # Close the connection and re-render the signup page with the entered data
        conn.close()
        return render_template(
            'signup_page.html',
            roll_no=roll_no,
            username=username,
            email_id=email_id,
            address=address,
            class1=class1
        )
