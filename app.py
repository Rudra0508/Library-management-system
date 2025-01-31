from flask import Flask,render_template
import sys

# Set path for modules
sys.path.insert(0, "C://Users//admin//Desktop//app//modules")

from modules.page1 import page1_bp                                     

from modules.login_page import login_bp                                

from modules.menu_page import menu_bp                                 

from modules.issue import issue_bp                                     

from modules.return_page import return_bp                             

from modules.display_all_books import display_book_bp                  

from modules.display_fine import display_fine_bp                       

from modules.insert_book import insert_bp                              

from modules.choose_role_page import choose_bp                         

from modules.signup_page import signup_bp                                



app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
def welcome():
    return render_template ("page1.html")


# Register Blueprints
app.register_blueprint(choose_bp,url_prefix='/choose')

app.register_blueprint(page1_bp,url_prefix='/page1')

app.register_blueprint(login_bp,url_prefix='/login')

app.register_blueprint(menu_bp, url_prefix='/menu')

app.register_blueprint(issue_bp, url_prefix='/issue')# Register issue blueprint

app.register_blueprint(return_bp, url_prefix='/return')

app.register_blueprint(display_book_bp, url_prefix='/display_books')

app.register_blueprint(display_fine_bp,url_prefix='/fine')

app.register_blueprint(insert_bp,url_prefix='/insert')

app.register_blueprint(signup_bp,url_prefix='/signup')




if __name__ == '__main__':
    app.run(debug=True)
