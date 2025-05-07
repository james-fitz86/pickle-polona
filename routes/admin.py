from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route("/")
def dashboard():
    """Home page for the app"""
    return render_template("/admin/dashboard.html")

@admin.route('/products')
def manage_products():
    """Admin page to view/manage products."""
    return render_template('admin/products.html')