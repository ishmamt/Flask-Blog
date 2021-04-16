from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    # for posting new blog
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Your Post', validators=[DataRequired()])
    submit = SubmitField('Post')
