from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

insert_bp=Blueprint('insert',__name__)

@insert_bp.route('/insert_page')
def insert_page():
    return render_template('insert_book.html')

@insert_bp.route('/submit_book', methods=['POST'])
def submit_books():
    try:
        action=request.form.get('action')
        book_name=request.form.get('book')


        if action=='submit':

            author_name=request.form['author']
            pub_name=request.form['publisher']
            copies1=request.form['copies']
            copies2=request.form['copies']

            conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
            cursor = conn.cursor()

            cursor.execute("select * from books_lib where NAME_BOOK=?",(book_name,))
            new1=cursor.fetchall()

            if not new1:
                
                cursor.execute("insert into books_lib (NAME_BOOK,AUTHOR_BOOK,PUB_BOOK,COPIES1,COPIES2)values(?,?,?,?,?)",(book_name,author_name,pub_name,copies1,copies2))
                conn.commit()

                flash("BOOK INSERTED!!!",'SUCCESS')
                return render_template("insert_book.html")

            else:

                flash("BOOK ALREADY INSERTED!!!", "error")
                return render_template("insert_book.html")
                

        elif action=="BACK":
            return render_template("menu_page.html")
        
    except Exception as e:
        logging.error(f'Error occurred: {e}')
        flash("An error occurred.", "error")
