from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(Form):
    email = StringField('Email', validators=[InputRequired(message='A email is required!'), Email(message='Mast be email format!')])
    password = PasswordField('Password', validators=[InputRequired(message='A password is required!'), Length(min=8, max=32, message='Mast be between 8 and 32 characters!')])
    pin = PasswordField('PIN', validators=[InputRequired(message='A pin is required!'), Length(min=4, max=8, message='Mast be between 4 and 8 characters!')])
    submit = SubmitField('Sign In')
