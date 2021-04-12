from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '6304b01155a34b592f575364199d8581'  # secret key for cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # relative path from where ever we are to site.db
db = SQLAlchemy(app)

from flaskblog import routes  # to prevent circular import
