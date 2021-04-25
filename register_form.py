from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    email = EmailField('eMail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10)])
    password_again = PasswordField('Repeat password', validators=[DataRequired(), Length(min=10)])
    nickname = StringField('Display name', validators=[DataRequired()])
    agree = BooleanField('I agree with Terms of Usage')
    submit = SubmitField('Sign Up')
