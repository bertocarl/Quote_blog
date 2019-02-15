from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField('Blog Category:', validators = [Required()])
    post = TextAreaField('Write your Blog:', validators = None)
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself',validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    name = StringField("Your Name")
    comment_itself = StringField("Comment",validators=[Required()])
    submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField("Enter Your Email Address :")
    submit= SubmitField('Subscribe')