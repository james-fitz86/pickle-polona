from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, Email

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=2, max=30)])
    email = StringField("Email address", validators=[InputRequired(), Email(), Length(max=50)])
    subject = StringField("Subject", validators=[InputRequired(), Length(min=3, max=50)])
    message = TextAreaField("Message", validators=[InputRequired(), Length(min=10, max=1000)])
    submit = SubmitField("Send Message")
