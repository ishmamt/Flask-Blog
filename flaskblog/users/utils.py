import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail, app
from flask_login import current_user


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f""" To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this message and no changes will take place.
    """
    mail.send(msg)
