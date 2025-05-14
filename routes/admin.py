from flask import Blueprint, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from forms.product_form import ProductForm
from models.product import Product
from extensions import db
from sqlalchemy import select
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')

load_dotenv()
admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")

@admin.before_request
def restrict_admin_pages():
    allowed_routes = ['admin.login', 'admin.login_action', 'admin.logout']
    if 'username' not in session and request.endpoint not in allowed_routes:
        
        session['next'] = request.path
        return redirect(url_for("admin.login"))

@admin.route("/")
def dashboard():
    """Admin main dashboard page"""
    return render_template("/admin/dashboard.html")

@admin.route("/admin-login-2025", methods=["GET"])
def login():
    """Display the admin login form if the user is not logged in."""

    if "username" in session:
        return redirect(url_for("admin.dashboard"))


    return render_template("/admin/admin_login.html")

@admin.route("/admin-login-2025", methods=["POST"])
def login_action():
    """Handle login form submission and authenticate the user."""

    username = request.form.get("username")
    password = request.form.get("password")

    if username == admin_username and password == admin_password:
        session["username"] = request.form["username"]
        return redirect(url_for("admin.dashboard"))
    
    return render_template("admin/admin_login.html", error="Invalid input")

@admin.route("/logout")
def logout():
    """Log out the user by clearing the session."""
    session.pop("username", None)

    return redirect(url_for("admin.login"))

@admin.route('/products')
def products():
    """Admin page to view/manage products."""
    stmt = select(Product)
    products = db.session.scalars(stmt)
    return render_template('admin/products.html', products=products)

@admin.route('/orders')
def orders():
    """Admin page to view/manage orders."""
    return render_template('admin/orders.html')

@admin.route('/stock_orders')
def stock_orders():
    """Admin page to view/manage stock orders."""
    return render_template('admin/stock_orders.html')

@admin.route('/messages')
def messages():
    """Admin page to view/manage contact messages."""
    return render_template('admin/messages.html')

@admin.route('/add_product', methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            sku=form.sku.data,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            size=form.size.data,
            category=form.category.data,
            ingredients=form.ingredients.data,
            featured=form.featured.data,
            image_main=form.image_main.data,
            image_1=form.image_1.data,
            image_2=form.image_2.data,
            stock_quantity=form.stock_quantity.data,
            in_stock=form.in_stock.data,
            expiry_date=form.expiry_date.data,
            stock_location=form.stock_location.data,
            packs_per_box=form.packs_per_box.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("admin.add_product"))
    else:
        return render_template("admin/add_product.html", form=form)

@admin.route("/product/<string:product_sku>")
def product(product_sku):
    stmt = select(Product).where(Product.sku == product_sku)
    product = db.session.scalars(stmt).first()
    return render_template("admin/product.html", product=product)