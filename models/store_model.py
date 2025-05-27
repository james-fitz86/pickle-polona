from extensions import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_reference = db.Column(db.String(20), unique=True, nullable=False, default=lambda: f"ORD-{int(datetime.utcnow().timestamp())}")

    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    county = db.Column(db.String(50))
    postcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = relationship('OrderItem', backref='order', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Order {self.order_reference} - {self.first_name} {self.surname}>"

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_sku = db.Column(db.String(20), db.ForeignKey('products.sku'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = relationship('Product')

    def __repr__(self):
        return f"<OrderItem SKU: {self.product_sku} x {self.quantity}>"

