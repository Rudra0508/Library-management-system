from flask import Blueprint, render_template, session, redirect, url_for

menu_bp = Blueprint('menu', __name__)

# Menu Page Route
@menu_bp.route('/menu_page')
def menu_page():
    if not session.get('logged_in'):
        return redirect(url_for('login.form'))
    return render_template('menu_page.html')
