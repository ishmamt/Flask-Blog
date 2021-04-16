from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '6304b01155a34b592f575364199d8581'  # secret key for cookies and generating reset tokens
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # relative path from where ever we are to site.db
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# getting from environment variables
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "users.login"  # the name of the function to handle log in page.
login_manager.login_message_category = "info"  # bootsrap class


# to prevent circular import
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
