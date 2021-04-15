import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)  # getting the page. Default page is 1
    # posts = Post.query.all()  # kept it here to show how I did it earlier
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)  # to prevent grabbing and loading all the posts at once
    return render_template("home.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html", title='about')


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # decode needed to get string hash
        # creating a new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}.", "success")
        return redirect(url_for("login"))
    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # returns none if next argument is not there
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check username or password.", "danger")
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # random name of the picture
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)

    # resizing the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # saving the image
    i.save(picture_path)

    # deleting the old profile pic
    old_pic = current_user.image_file
    old_pic_path = os.path.join(app.root_path, 'static/profile_pic', old_pic)
    if old_pic != 'default.jpg' and os.path.exists(old_pic_path):
        os.remove(old_pic_path)

    return picture_fn


@app.route('/edit_profile', methods=["GET", "POST"])
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
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pic/{current_user.image_file}')
    return render_template("account.html", title="edit profile", image_file=image_file, form=form)


@app.route('/post/new', methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("New post created.", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title='new post', form=form, legend='Create Post')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("The post has been updated.", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title='edit', form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    db.session.delete(post)
    db.session.commit()
    flash("The post has been deleted.", "success")
    return redirect(url_for("home"))


@app.route('/<string:username>', methods=["GET", "POST"])
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("user_posts.html", posts=posts, user=user, title=user.username)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f""" To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this message and no changes will take place.
    """
    mail.send(msg)


@app.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('If an account with this email address exists, an email has been sent with instructions to the specified email.', "info")
            return redirect(url_for("login"))
        else:
            flash('If an account with this email address exists, an email has been sent with instructions to the specified email.', "info")
            return redirect(url_for("login"))
    return render_template("reset_request.html", title="reset password", form=form)


@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or expired.', "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # decode needed to get string hash
        # creating a new user
        user.password = hashed_password
        db.session.commit()

        flash(f"Your password has been updated!", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="reset password", form=form)
