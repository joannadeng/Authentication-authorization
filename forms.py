from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired, Email, Length
import email_validator

class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username",validators=[InputRequired(),Length(min=1,max=20)])
    password = PasswordField('Password',validators=[InputRequired()])
    email = StringField('Email Address',validators=[InputRequired(),Email(),Length(max=50)])
    first_name = StringField('First Name',validators=[InputRequired(),Length(max=30)])
    last_name = StringField('Last Name',validators=[InputRequired(),Length(max=30)])
    # is_admin = RadioField('Is Admin',default='False')

class LoginForm(FlaskForm):
    """Form for login"""

    username = StringField("Username",validators=[InputRequired(),Length(min=1,max=30)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=4,max=20)])

class FeedbackForm(FlaskForm):
    """Form for adding and editing feedback"""

    title = StringField('Title',validators=[InputRequired(),Length(max=100)])
    content = StringField('Content',validators=[InputRequired()])