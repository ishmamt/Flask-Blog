from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '6304b01155a34b592f575364199d8581'  # secret key for cookies


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


if __name__ == '__main__':
    app.run(debug=True)
