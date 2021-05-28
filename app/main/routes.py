from flask import render_template

from app import db
from app.models import Category, Product

from app.main import bp


@bp.route('/')
def index():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('base.html', categories=categories, products=products)
