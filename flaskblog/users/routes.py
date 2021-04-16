from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)  # similar to app = Flask(__name__)


@users.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # decode needed to get string hash
        # creating a new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}.", "success")
        return redirect(url_for("users.login"))
    return render_template('register.html', title='register', form=form)


@users.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # returns none if next argument is not there
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check username or password.", "danger")
    return render_template('login.html', title='login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route('/edit_profile', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account has been updated.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pic/{current_user.image_file}')
    return render_template("account.html", title="edit profile", image_file=image_file, form=form)


@users.route('/<string:username>', methods=["GET", "POST"])
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("user_posts.html", posts=posts, user=user, title=user.username)


@users.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('If an account with this email address exists, an email has been sent with instructions to the specified email.', "info")
            return redirect(url_for("users.login"))
        else:
            flash('If an account with this email address exists, an email has been sent with instructions to the specified email.', "info")
            return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="reset password", form=form)


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or expired.', "warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # decode needed to get string hash
        # creating a new user
        user.password = hashed_password
        db.session.commit()

        flash(f"Your password has been updated!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="reset password", form=form)