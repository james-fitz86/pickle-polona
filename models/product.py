from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    sku = db.mapped_column(db.String(20), primary_key=True)
    name = db.mapped_column(db.String(100), nullable=False)
    description = db.mapped_column(db.Text, nullable=False)

    price = db.mapped_column(db.Float, nullable=False)
    size = db.mapped_column(db.String(50))

    category = db.mapped_column(db.String(50))
    ingredients = db.mapped_column(db.Text)

    is_vegan = db.mapped_column(db.Boolean, default=False)
    is_gluten_free = db.mapped_column(db.Boolean, default=False)
    featured = db.mapped_column(db.Boolean, default=False)

    image_main = db.mapped_column(db.String(200))
    image_1 = db.mapped_column(db.String(200))
    image_2 = db.mapped_column(db.String(200))

    stock_quantity = db.mapped_column(db.Integer, nullable=False, default=0)
    in_stock = db.mapped_column(db.Boolean, default=True)

    expiry_date = db.mapped_column(db.Date)
    location = db.mapped_column(db.String(100))

    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
    updated_at = db.mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.sku} - {self.name}>"