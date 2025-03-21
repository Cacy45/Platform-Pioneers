from flask import Flask #, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from extensions import db, init_db
#from models import *

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_grievances.db'

    db.init_app(app)

    #imports later
    from .routes.routes import register_routes
    register_routes(app,db)


    migrate = Migrate(app,db)

    return app

"""
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_grievances.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
init_db(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student_login')
def student_login():
    return render_template('student_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/student_signup')
def student_signup():
    return render_template('student_signup.html')



if __name__ == '__main__':
    app.run(debug=True)"
"""