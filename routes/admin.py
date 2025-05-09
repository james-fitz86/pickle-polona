from flask import Blueprint, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')

admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")

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
    return render_template('admin/products.html')

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
