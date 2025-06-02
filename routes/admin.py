from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import date
from dotenv import load_dotenv
from forms.product_form import ProductForm
from forms.stock_form import StockForm
from models.product import Product, Batch, BatchAllocation
from models.store_model import Order, OrderStatus, OrderItem
from models.admin_model import fulfill_order, ship_order
from models.main_model import ContactMessage
from extensions import db
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
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
        flash(f"{username} successfully logged in!")
        return redirect(url_for("admin.dashboard"))
    
    return render_template("admin/admin_login.html", error="Invalid input")

@admin.route("/logout")
def logout():
    """Log out the user by clearing the session."""
    username = session.get("username")
    session.pop("username", None)
    
    flash(f"{username} successfully logged Out!")
    return redirect(url_for("admin.login"))

@admin.route('/products')
def products():
    """Admin page to view/manage products and filter by active."""
    active_paramater= request.args.get("active")
    stmt = select(Product).options(selectinload(Product.batches))

    active_filter = None

    if active_paramater is not None:
        active_filter = active_paramater.lower() == ("true")
        stmt = stmt.where(Product.active == active_filter)

    products = db.session.scalars(stmt).all()
    return render_template('admin/products.html', products=products, selected_active=active_paramater)

@admin.route('/orders')
def orders():
    """Admin page to view/manage orders and filter by status."""
    status_filter = request.args.get("status", type=str)

    stmt = select(Order).options(selectinload(Order.order_items))

    if status_filter:
        stmt = stmt.where(Order.status == OrderStatus(status_filter.lower()))

    stmt = stmt.order_by(Order.created_at.desc())
    orders = db.session.scalars(stmt).all()
    return render_template('admin/orders.html', orders=orders, selected_status=status_filter)

@admin.route("/order/<int:id>")
def order(id):
    "Admin page to display individual Order"
    stmt = select(Order).where(Order.id == id)
    order = db.session.scalars(stmt).first()
    order_items = order.order_items
    return render_template("admin/order.html", order=order, order_items=order_items, OrderStatus=OrderStatus)

@admin.route('/stock_batches')
def stock_batches():
    """Admin page to view/manage stock batches."""
    stock_filter = request.args.get('stock')

    stmt = select(Batch)
    all_batches = db.session.scalars(stmt)

    if stock_filter == 'remaining':
        filtered_batches = [ b for b in all_batches if b.stock_quantity > 0]
    elif stock_filter == 'none':
        filtered_batches = [ b for b in all_batches if b.stock_quantity == 0]
    else:
        filtered_batches = all_batches

    batches_sorted = sorted(filtered_batches, key=lambda b: b.expiry_date)

    return render_template('admin/stock_batches.html', batches=batches_sorted, selected_stock=stock_filter)

@admin.route('/messages')
def messages():
    """Admin page to view/manage contact messages with pagination."""
    page = request.args.get('page', 0, type=int)
    per_page = int(os.getenv("MESSAGES_PER_PAGE", 10))

    total_messages = db.session.scalar(
        db.select(db.func.count()).select_from(ContactMessage)
    )
    total_pages = (total_messages + per_page - 1) // per_page 

    stmt = (
        select(ContactMessage)
        .order_by(ContactMessage.submitted_at.desc())
        .limit(per_page)
        .offset(page * per_page)
    )
    messages = db.session.scalars(stmt).all()

    return render_template('admin/messages.html', messages=messages, page=page, total_pages=total_pages)

@admin.route('/add_product', methods=["GET", "POST"])
def add_product():
    """Admin Page to add Products"""
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
            active=form.active.data,
            packs_per_box=form.packs_per_box.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("admin.add_product"))
    else:
        return render_template("admin/add_product.html", form=form)

@admin.route("/product/<string:product_sku>")
def product(product_sku):
    "Admin page to display individual Product"
    stmt = select(Product).where(Product.sku == product_sku)
    product = db.session.scalars(stmt).first()
    batches = product.batches
    batches_sorted = sorted(batches, key=lambda b: b.expiry_date)
    return render_template("admin/product.html", product=product, batches=batches_sorted)

@admin.route("/product/<string:product_sku>/edit", methods=["GET", "POST"])
def edit_product(product_sku):
    """Admin page to edit indivual Product"""
    product = db.session.scalar(select(Product).where(Product.sku == product_sku))

    form = ProductForm(obj=product)
    form.submit.label.text = "Save Changes"

    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        return redirect(url_for("admin.product", product_sku=product.sku))

    return render_template("admin/edit_product.html", form=form, product=product)

@admin.route('/stock_batch/', methods=['GET', 'POST'])
def stock_batch():
    """Admin page to add a stock batch"""
    form = StockForm()

    form.product_sku.choices = [(product.sku, f"{product.sku} - {product.name}") for product in Product.query.all()]

    if form.validate_on_submit():
        batch = Batch(
            stock_quantity=form.stock_quantity.data,
            stock_location=form.stock_location.data,
            expiry_date=form.expiry_date.data,
            product_sku=form.product_sku.data
        )
        db.session.add(batch)
        db.session.commit()
        flash("Stock batch added!", "success")
        return redirect(url_for('admin.stock_batch'))

    return render_template('admin/stock_batch.html', form=form)

@admin.route("/stock_batch/<int:id>/edit", methods=["GET", "POST"])
def edit_batch(id):
    """Admin page to edit individual Batch from Batches page"""
    batch = db.session.scalar(select(Batch).where(Batch.id == id))

    form = StockForm(obj=batch)
    form.product_sku.choices = [(product.sku, f"{product.sku} - {product.name}") for product in Product.query.all()]

    form.submit.label.text = "Save Changes"

    if form.validate_on_submit():
        form.populate_obj(batch)
        db.session.commit()
        return redirect(url_for("admin.stock_batches", id=batch.id))

    return render_template("admin/edit_batch.html", form=form, batch=batch)

@admin.route("/product/<string:product_sku>/<int:id>/edit", methods=["GET", "POST"])
def edit_product_batch(id, product_sku):
    """Admin page to edit individual Batch from Product page"""
    batch = db.session.scalar(select(Batch).where(Batch.id == id))
    product = db.session.scalar(select(Product).where(Product.sku == product_sku))

    form = StockForm(obj=batch)
    form.product_sku.choices = [(product.sku, f"{product.sku} - {product.name}") for product in Product.query.all()]

    form.submit.label.text = "Save Changes"

    if form.validate_on_submit():
        form.populate_obj(batch)
        db.session.commit()
        return redirect(url_for("admin.product", product_sku=product.sku))

    return render_template("admin/edit_product_batch.html", form=form, batch=batch)

@admin.route("/stock_batch/<int:id>/delete", methods=["GET"])
def delete_batch(id):
    """Admin page to delete individual Batch from Batches page"""
    batch = db.session.scalar(select(Batch).where(Batch.id == id))

    today = date.today()

    if batch.stock_quantity > 0 and batch.expiry_date >= today:
        flash("You cannot delete a batch with usable stock", "warning")
        return redirect(url_for("admin.stock_batches"))
    
    db.session.delete(batch)
    db.session.commit()
    flash(f"Deleted batch with ID: {batch.id}", "success")

    return redirect(url_for("admin.stock_batches"))

@admin.route("/product/<string:product_sku>/<int:id>/delete", methods=["GET"])
def delete_product_batch(id, product_sku):
    """Admin page to delete individual Batch from Product page"""
    batch = db.session.scalar(select(Batch).where(Batch.id == id))
    product = db.session.scalar(select(Product).where(Product.sku == product_sku))

    db.session.delete(batch)
    db.session.commit()
    flash(f"Deleted batch with ID: {batch.id}")

    return redirect(url_for("admin.product", product_sku=product.sku))

@admin.route('/orders/<int:order_id>/fulfill')
def fulfill_order_view(order_id):
    order = Order.query.options(
        joinedload(Order.order_items)
        .joinedload(OrderItem.batch_allocations)
        .joinedload(BatchAllocation.batch)
    ).get_or_404(order_id)

    try:
        from models.admin_model import fulfill_order
        picklist = fulfill_order(order)

        skus = [item.product_sku for item in order.order_items]
        product_names = {
        product.sku: product.name
        for product in Product.query.filter(Product.sku.in_(skus)).all()
        }

        return render_template("admin/picklist.html", order=order, picklist=picklist, product_names=product_names)
    
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.order", id=order.id))
    
@admin.route('/orders/<int:order_id>/picklist')
def picklist_view(order_id):
    order = Order.query.options(
        joinedload(Order.order_items)
        .joinedload(OrderItem.batch_allocations)
        .joinedload(BatchAllocation.batch)
    ).get_or_404(order_id)

    if order.status != OrderStatus.fulfilled:
        flash("Picklist available only for fulfilled orders.", "warning")
        return redirect(url_for("admin.order", id=order.id))

    picklist = []
    for item in order.order_items:
        item_info = {
            "product_sku": item.product_sku,
            "quantity": item.quantity,
            "allocations": []
        }
        for allocation in item.batch_allocations:
            item_info["allocations"].append({
                "batch_id": allocation.batch_id,
                "quantity": allocation.quantity_deducted,
                "location": allocation.batch.stock_location
            })
        picklist.append(item_info)
    
    skus = [item.product_sku for item in order.order_items]
    product_names = {
        product.sku: product.name
        for product in Product.query.filter(Product.sku.in_(skus)).all()
    }


    return render_template("admin/picklist.html", order=order, picklist=picklist, product_names=product_names)

@admin.route('/orders/<int:order_id>/ship', methods=["POST"])
def ship_order_view(order_id):
    order = Order.query.get_or_404(order_id)

    try:
        from models.admin_model import ship_order
        ship_order(order)
        flash("Order marked as shipped.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("admin.order", id=order.id))
