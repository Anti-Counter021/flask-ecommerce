from app import create_app, db
from app.cart_search import get_cart
from app.models import (
    Category,
    Product,
    User,
    CartProduct,
    Cart,
    Testimonial,
    Order,
    CategoryFeature,
    ProductFeature
)

app = create_app()


@app.context_processor
def categories_testimonials():
    """ Context categories """
    return {'categories': Category.query.all(), 'testimonials_count': Testimonial.query.count()}


@app.context_processor
def cart():
    """ Context cart """
    return {'cart': get_cart()}


@app.shell_context_processor
def make_shell_context():
    """ Shell context """
    return {
        'db': db, 'Category': Category, 'Product': Product, 'User': User, 'CartProduct': CartProduct, 'Cart': Cart,
        'Testimonial': Testimonial, 'Order': Order, 'CategoryFeature': CategoryFeature, 'ProductFeature': ProductFeature
    }
