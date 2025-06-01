from extensions import db
from sqlalchemy import asc
from flask import flash
from models.product import Batch
from models.store_model import OrderStatus

def deduct_stock_by_expiry(sku, quantity_needed):
    """
    Deducts stock by expiry. Returns list of (batch_id, quantity_deducted) if successful,
    or None if insufficient stock.
    """
    batches = Batch.query.filter_by(product_sku=sku)\
        .filter(Batch.stock_quantity > 0)\
        .order_by(asc(Batch.expiry_date)).all()

    total_available = sum(batch.stock_quantity for batch in batches)
    if total_available < quantity_needed:
        flash(f"Not enough stock available for SKU {sku}.", "danger")
        return None

    allocations = []

    for batch in batches:
        if quantity_needed <= 0:
            break
        to_deduct = min(batch.stock_quantity, quantity_needed)
        batch.stock_quantity -= to_deduct
        allocations.append((batch.id, to_deduct))
        quantity_needed -= to_deduct

    return allocations

def fulfill_order(order):
    """
    Marks the given order as fulfilled and returns a picklist of batch allocations and locations.
    """
    if order.status != OrderStatus.pending:
        raise ValueError("Only pending orders can be fulfilled.")

    picklist = []

    for item in order.order_items:
        item_info = {
            "product_sku": item.product_sku,
            "quantity": item.quantity,
            "allocations": []
        }
        for allocation in item.batch_allocations:
            location = allocation.batch.stock_location
            item_info["allocations"].append({
                "batch_id": allocation.batch_id,
                "quantity": allocation.quantity_deducted,
                "location": location
            })
        picklist.append(item_info)

    order.status = OrderStatus.fulfilled
    db.session.commit()

    return picklist

def ship_order(order):
    """Marks the given order as shipped"""
    if order.status != OrderStatus.fulfilled:
        raise ValueError("Only fulfilled orders can be shipped.")
    
    order.status = OrderStatus.shipped
    db.session.commit()