from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, TextAreaField, SubmitField, DateField
from wtforms.validators import InputRequired, Optional, Length

class ProductForm(FlaskForm):
    sku = StringField("SKU", validators=[InputRequired(), Length(max=20)])
    name = StringField("Name", validators=[InputRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[InputRequired()])

    price = FloatField("Price", validators=[InputRequired()])
    size = StringField("Size", validators=[Optional(), Length(max=50)])
    category = StringField("Category", validators=[Optional(), Length(max=50)])
    ingredients = TextAreaField("Ingredients", validators=[Optional()])

    featured = BooleanField("Featured")

    image_main = StringField("Main Image Filename", validators=[Optional(), Length(max=200)])
    image_1 = StringField("Image 1 Filename", validators=[Optional(), Length(max=200)])
    image_2 = StringField("Image 2 Filename", validators=[Optional(), Length(max=200)])
    
    in_stock = BooleanField("In Stock", default=True)
    packs_per_box = IntegerField("Packs Per Box", validators=[InputRequired()])

    submit = SubmitField("Add Product")