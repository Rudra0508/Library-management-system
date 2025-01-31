from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import sqlite3

login_bp = Blueprint('login', __name__)  # Define a blueprint for login-related routes

# Login Page route
@login_bp.route('/login1')
def form():
    role = request.args.get('role', 'student')  # Default role is student
    role_message = "Please log in as Admin" if role == "admin" else "Please log in as Student"
    session['role'] = role  # Save role in session
    return render_template('login_page.html', role=role, role_message=role_message)


# Login Submission route
@login_bp.route('/submit', methods=['POST'])
def submit_form():
    username = request.form['username']
    password = request.form['password']
    role = session.get('role', 'student')  # Retrieve role from session

    action = request.form.get("action")

    if action == "submit":
        # Admin Login Check
        if role == "admin" and username == "admin01" and password == "12345":
            session['logged_in'] = True
            session['user_role'] = "admin"  # Store role
            session['username'] = "admin01"  # Store username
            session['roll_no'] = None       # Admin doesn't need roll_no
            return redirect(url_for('menu.menu_page'))

        # Connect to the SQLite database for student login
        conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
        cursor = conn.cursor()

        # Validate the username and retrieve user details
        cursor.execute("SELECT * FROM student_id WHERE name=?", (username,))
        user = cursor.fetchone()

        conn.close()

        # If user not found
        if not user:
            flash("USERNAME NOT FOUND!!", "error")
            return render_template('login_page.html', role=role)

        # Student Login: Validate both username and password
        if role == "student" and password == str(user[5]):  # Assuming password is at index 5
            session['logged_in'] = True
            session['user_role'] = "student"  # Store role
            session['username'] = user[1]     # Assuming username is at index 1
            session['roll_no'] = user[0]      # Assuming roll_no is at index 0
            return redirect(url_for('menu.menu_page'))

        # Wrong Password
        flash("WRONG PASSWORD!!", "error")
        return render_template('login_page.html', role=role)

    elif action == "SIGNUP":
        # Redirect to Signup Page
        return render_template("signup_page.html")


