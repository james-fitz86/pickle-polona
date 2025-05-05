from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    """Home page for the app"""
    return render_template("index.html")

@app.route("/store")
def store():
    """Storefront page for the app"""
    return render_template("store.html")

@app.route("/about")
def about():
    """About page for the app"""
    return render_template("about.html")

@app.route("/contact")
def contact():
    """Contact page for the app"""
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)