from flask_login import current_user

from app import create_app, db
from app.models import Category, Product, User, CartProduct, Cart

app = create_app()


@app.context_processor
def categories():
    return {'categories': Category.query.all()}


@app.context_processor
def cart():
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
    return {'cart': cart_}


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'Product': Product, 'User': User, 'CartProduct': CartProduct, 'Cart': Cart}
