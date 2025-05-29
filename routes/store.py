from flask import Blueprint, render_template, request, redirect, url_for, json, flash
from sqlalchemy import select
from models.product import Product
from models.store_model import Order, OrderItem
from forms.checkout_form import CheckoutForm
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


@store.route('/checkout', methods=["GET", "POST"])
def checkout():
    """Checkout page for placing an order"""
    form = CheckoutForm()

    if form.validate_on_submit():
        cart_json = request.form.get("cart_json")
        cart_items = json.loads(cart_json) if cart_json else []

        for item in cart_items:
            product = Product.query.filter_by(sku=item["product_sku"]).first()
            if not product:
                flash(f"Product with SKU {item['product_sku']} not found.", "danger")
                return redirect(url_for("store.cart"))

            if float(item["price"]) != float(product.price):
                flash(f"Price mismatch for {product.name}. Please refresh your cart.", "danger")
                return redirect(url_for("store.cart"))

        
        new_order = Order(
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address_line1=form.address_line1.data,
            address_line2=form.address_line2.data,
            city=form.city.data,
            county=form.county.data,
            postcode=form.postcode.data,
            country=form.country.data
        )

        db.session.add(new_order)
        db.session.flush()

        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_sku=item["product_sku"],
                quantity=item["quantity"]
            )
            db.session.add(order_item)

        db.session.commit()
        return redirect(url_for("store.success"))

    return render_template("checkout.html", form=form)

@store.route("/order_success")
def success():
    """Order Success page"""
    return render_template("order_success.html")