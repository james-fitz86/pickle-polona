from flask import Blueprint, render_template

store = Blueprint('store', __name__)

@store.route("/store")
def storefront():
    """Storefront page for the app"""
    return render_template("store.html")