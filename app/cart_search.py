from flask_login import current_user

from app import db
from app.models import Cart


def get_cart():
    """ Get cart """
    if current_user.is_authenticated:
        cart_ = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart_:
            cart_ = Cart(user_id=current_user.id)
            db.session.add(cart_)
            db.session.commit()
    else:
        cart_ = Cart.query.filter_by(for_anonymous_user=True).first()
        if not cart_:
            cart_ = Cart(for_anonymous_user=True)
            db.session.add(cart_)
            db.session.commit()
    return cart_


def recalculate_cart(cart):
    """ Recalculate count and price product in cart """
    cart_count = cart.products.count()
    cart_sum = 0
    for item in cart.products.all():
        cart_sum += item.final_price
    cart.final_price = cart_sum
    cart.total_products = cart_count
    db.session.commit()
