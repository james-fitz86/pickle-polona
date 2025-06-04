from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from models.main_model import ContactMessage, years_since_feb_2024
from forms.contact_form import ContactForm
from models.product import Product
from extensions import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    """Home page for the app"""
    featured_products= Product.query.filter_by(featured=True).all()
    return render_template("index.html", products=featured_products)

@main.route("/about")
def about():
    """About page for the app"""
    years = years_since_feb_2024()
    return render_template('about.html', years_since=years)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page for the app"""
    form = ContactForm()

    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash("Your message has been sent. Thank you!", "success")
        return redirect(url_for("main.contact", success=True))

    success = request.args.get("success")
    return render_template("contact.html", form=form, success=success)

@main.route('/raise_500')
def raise_500_error():
    """Manually raise a 500 Internal Server Error (for testing & demonstration)."""
    abort(500)

def register_error_handlers(app):
    """Register custom error pages for 404 and 500 errors."""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html', error=error), 500