from flask import render_template, url_for, flash, redirect
from flaskblog.models import User, Post
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm


# fake database call
posts = [
    {
        'name': 'Ishmam Tashdeed',
        'content_name': 'Blog 1 Test',
        'date_posted': '07 April, 2021',
        'content': 'Hello world! My first ever test blog.'
    },
    {
        'name': 'Sarni V.',
        'content_name': 'The truth',
        'date_posted': '08 April, 2021',
        'content': 'I am The Cutest.'
    }
]


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template("home.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html", title='about')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}.", "success")
        return redirect(url_for("home"))
    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "1234":
            flash(f"Welcome Back {form.username.data}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please try again.", "danger")
    return render_template('login.html', title='login', form=form)
