from datetime import datetime
from flaskblog import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # for generating a timed encrypted signature
from flask_login import UserMixin  # for certain functions to control login sessions


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


# each class is a table in database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # will be hashed to 20 chars
    password = db.Column(db.String(60), nullable=False)  # will be hashed to 60 chars
    # one to many relationship. Lazy loads in data as needed. Backref is a reference.
    posts = db.relationship('Post', backref='author', lazy=True)  # refers to the Post class

    def get_reset_token(self, expires_sec=900):
        # returns the token with a payload and an exipartion time limit (defaulting to 15 minutes)
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']  # if token has not expired
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # refers to the id column in user table. Not class.

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
