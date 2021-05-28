from flask import render_template

from app.models import Category, Product

from app.main import bp


@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('base.html', products=products, header=1)


@bp.route('/category/<slug>')
def category_detail(slug):
    category = Category.query.filter_by(slug=slug).first()
    return render_template('category_detail.html', category=category, title=f'Category - {category.name}')


@bp.route('/category/<category_slug>/products/<product_slug>')
def product_detail(category_slug, product_slug):
    product = Product.query.filter_by(slug=product_slug).first()
    return render_template('product_detail.html', product=product, title=f'Product - {product.title}')
