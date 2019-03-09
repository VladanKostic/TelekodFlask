from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MockdataForm(FlaskForm):
    id = StringField('ID:', validators=[DataRequired()])
    firstname = StringField('First name:', validators=[DataRequired()])
    lastname = StringField('Last name:', validators=[DataRequired()])
    address = StringField('Address:', validators=[DataRequired()])
    dataofbirth = StringField('Data for birth:', validators=[DataRequired()])
    payment = StringField('Payment:', validators=[DataRequired()])
