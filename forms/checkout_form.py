from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class CheckoutForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])

    address_line1 = StringField('Address Line 1', validators=[DataRequired(), Length(max=100)])
    address_line2 = StringField('Address Line 2', validators=[Length(max=100)])
    city = StringField('City / Town', validators=[DataRequired(), Length(max=50)])
    county = StringField('County / State', validators=[Length(max=50)])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=50)])

    submit = SubmitField('Place Order')
