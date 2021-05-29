from app import create_app, db
from app.cart_search import get_cart
from app.models import Category, Product, User, CartProduct, Cart

app = create_app()


@app.context_processor
def categories():
    """ Context categories """
    return {'categories': Category.query.all()}


@app.context_processor
def cart():
    """ Context cart """
    return {'cart': get_cart()}


@app.shell_context_processor
def make_shell_context():
    """ Shell context """
    return {'db': db, 'Category': Category, 'Product': Product, 'User': User, 'CartProduct': CartProduct, 'Cart': Cart}
