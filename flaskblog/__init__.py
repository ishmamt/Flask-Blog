from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '6304b01155a34b592f575364199d8581'  # secret key for cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # relative path from where ever we are to site.db
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # the name of the function to handle log in page.
login_manager.login_message_category = "info"  # bootsrap class

from flaskblog import routes  # to prevent circular import
