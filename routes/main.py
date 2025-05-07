from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    """Home page for the app"""
    return render_template("index.html")

@main.route("/about")
def about():
    """About page for the app"""
    return render_template("about.html")

@main.route("/contact")
def contact():
    """Contact page for the app"""
    return render_template("contact.html")