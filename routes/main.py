from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.main_model import ContactMessage
from forms.contact_form import ContactForm
from extensions import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    """Home page for the app"""
    return render_template("index.html")

@main.route("/about")
def about():
    """About page for the app"""
    return render_template("about.html")

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