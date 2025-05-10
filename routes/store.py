from flask import Blueprint, render_template
from sqlalchemy import select
from models.product import Product
from extensions import db

store = Blueprint('store', __name__)

@store.route("/store")
def storefront():
    """Storefront page for the app"""
    stmt = select(Product)
    print(stmt, flush=True)
    products = db.session.scalars(stmt)
    return render_template("store.html", products=products)