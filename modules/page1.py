from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import logging

logging.basicConfig(level=logging.DEBUG)


page1_bp = Blueprint('page1', __name__)  # Define a blueprint for issue book-related routes

@page1_bp.route('/page1_code')
def page1_code():
    return render_template('choose_role_page.html')