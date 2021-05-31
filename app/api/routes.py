from flask import jsonify, request, render_template

from app.models import Category, Product, Testimonial
from app.api import bp


def category_get_for_slug(slug):
    """ Get category for slug """
    return Category.query.filter_by(slug=slug).first()


@bp.route('/')
def index():
    """ Api navigation """
    categories = Category.query.all()
    products = Product.query.all()
    testimonials = Testimonial.query.all()
    return render_template('api/api_base.html', title='API', categories=categories, products=products,
                           testimonials=testimonials)


@bp.route('/categories')
def get_categories():
    """ Get all categories """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(Category.query, page, per_page, 'api.get_categories')
    return jsonify(data)


@bp.route('/category/<slug>')
def get_category(slug):
    """ Get category """
    return jsonify(category_get_for_slug(slug).to_dict())


@bp.route('/category/<slug>/products')
def get_products_for_category(slug):
    """ Get all products for category """
    category = category_get_for_slug(slug)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(Product.query.filter_by(category=category), page, per_page,
                                       'api.get_products_for_category', slug=slug)
    return jsonify(data)


@bp.route('/category/<category_slug>/product/<slug>')
def get_product(slug, category_slug):
    """ Get product """
    return jsonify(Product.query.filter_by(slug=slug).first().to_dict())


@bp.route('/products')
def get_all_products():
    """ Get all products """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_all_products')
    return jsonify(data)


@bp.route('/testimonial/<id>')
def get_testimonial(id):
    """ Get testimonial """
    return jsonify(Testimonial.query.get(id).to_dict())


@bp.route('/testimonials')
def get_testimonials():
    """ Get testimonials """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Testimonial.to_collection_dict(Testimonial.query, page, per_page, 'api.get_testimonials')
    return jsonify(data)
