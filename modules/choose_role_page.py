from flask import Blueprint, render_template

choose_bp = Blueprint("choose", __name__)

# Route for the admin menu
@choose_bp.route("/admin")
def admin_menu():
    return render_template("login_page.html", role="admin")  # Pass 'admin' role to the template

# Route for the user menu
@choose_bp.route("/user")
def user_menu():
    return render_template("login_page.html", role="student")  # Pass 'user' role to the template
