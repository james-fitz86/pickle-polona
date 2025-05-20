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

    featured = db.mapped_column(db.Boolean, default=False)

    image_main = db.mapped_column(db.String(200))
    image_1 = db.mapped_column(db.String(200))
    image_2 = db.mapped_column(db.String(200))

    in_stock = db.mapped_column(db.Boolean, default=True)

    packs_per_box = db.mapped_column(db.Integer, nullable=False, default=0)

    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
    updated_at = db.mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    batches = db.relationship('Batch', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.sku} - {self.name}>"
    
class Batch(db.Model):
    __tablename__ = 'batches'

    id = db.Column(db.Integer, primary_key=True)
    stock_quantity = db.mapped_column(db.Integer, nullable=False, default=0)
    stock_location = db.mapped_column(db.String(100))
    expiry_date = db.mapped_column(db.Date)
    product_sku = db.mapped_column(db.String, db.ForeignKey('products.sku'), nullable=False)

    def __repr__(self):
        return f"<Batch {self.id} - SKU: {self.product_sku}, Qty: {self.stock_quantity}>"