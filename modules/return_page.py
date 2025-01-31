from flask import Blueprint, Flask , render_template , request , redirect , url_for , flash
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)


return_bp=Blueprint('return',__name__)

@return_bp.route("/return_page")
def return_page():
    return render_template("return_page.html")


@return_bp.route("/SHOW_or_BACK", methods=['POST'])
def SHOW_or_BACK():
    try:
        action = request.form.get('action')

        if action == 'SHOW':
            roll_no = request.form['roll_no']
            book_name = request.form['book_name']

            # Connect to the database
            conn = sqlite3.connect(r"C:\Users\admin\Desktop\app\db1.db")
            cursor = conn.cursor()

            # Corrected SQL query
            cursor.execute("SELECT * FROM STUDENT_LIB WHERE roll_no=? AND book_name=?", (roll_no, book_name))
            issued_book = cursor.fetchall()

            if not issued_book:
                
                flash("BOOK NOT ISSUED!!!", "error")
                return render_template("return_page.html")
            else:
               
               
                flash("BOOK ISSUED!!!", "success")
                date_of_issue=issued_book[0][5]
                date_of_return=issued_book[0][6]

                cursor.execute("select DATE('now')")
                todays_date=cursor.fetchone()[0]

                cursor.execute("SELECT JULIANDAY(?) - JULIANDAY(?)", (todays_date, date_of_issue))
                days_issued = cursor.fetchone()[0]

                if days_issued > 30:
                    fine = int((days_issued - 30) * 2)  # Fine is 2 rupees per day overdue
                else:
                    fine = 0  # No fine if within 30 days

                return render_template("return_page.html",roll_no=roll_no,book_name=book_name,date_of_issue=date_of_issue,date_of_return=date_of_return,todays_date=todays_date,fine=fine)

            # Close the database connection
            conn.close()

        elif action == 'BACK':
            return render_template('menu_page.html')
        elif action=='CLEAR':
            return render_template('return_page.html')

    except Exception as e:
        logging.error(f'Error occurred: {e}')
        flash("An error occurred.", "error")
