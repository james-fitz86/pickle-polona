from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, SubmitField, SelectField
from wtforms.validators import InputRequired, Optional, Length, DataRequired

class StockForm(FlaskForm):
    stock_quantity = IntegerField("Stock Quantity", validators=[InputRequired()])
    stock_location = StringField("Stock Location", validators=[Optional(), Length(max=100)])
    expiry_date = DateField("Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])
    product_sku = SelectField("Product SKU", choices=[], validators=[InputRequired()])

    submit = SubmitField("Add Stock")
