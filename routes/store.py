from flask import Blueprint, render_template
from sqlalchemy import select
from models.product import Product
from extensions import db

store = Blueprint('store', __name__)

@store.route("/store")
def storefront():
    """Storefront page for the app"""
    stmt = select(Product)
    products = db.session.scalars(stmt)
    return render_template("store.html", products=products)

@store.route("/item/<string:product_sku>")
def item(product_sku):
    """Indivual Product page"""
    stmt = select(Product).where(Product.sku == product_sku)
    product = db.session.scalars(stmt).first()
    return render_template("item.html", product=product)

@store.route("/cart")
def cart():
    """Shopping Cart page for the app"""
    return render_template("cart.html")