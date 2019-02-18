from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField("Blog Title",validators=[Required()])
    blog = TextAreaField('Write your new blog here')
    category = SelectField("Blog category",choices=[('Information & Technology','Technology Blog'),('Food & Recipies','Food Blog'),('Fashion & Style','Fashion Blog'),('Sports & Fitness', 'Sports Blog')],validators=[Required()])
    submit = SubmitField('Post')

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Tell us about yourself.",validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment')
    submit = SubmitField('Submit')
class SubscribeForm(FlaskForm):
    email = StringField("Enter Your Email Address :")
    submit= SubmitField('Subscribe')