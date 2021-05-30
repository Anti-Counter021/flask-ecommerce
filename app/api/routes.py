from flask import jsonify, request

from app.models import Category, Product
from app.api import bp


def category_get_for_slug(slug):
    return Category.query.filter_by(slug=slug).first()


@bp.route('/categories')
def get_categories():
    """ Get all categories """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(Category.query, page, per_page, 'api.get_categories')
    return jsonify(data)


@bp.route('/category/<slug>')
def get_category(slug):
    return jsonify(category_get_for_slug(slug).to_dict())


@bp.route('/category/<slug>/products')
def get_products_for_category(slug):
    category = category_get_for_slug(slug)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(Product.query.filter_by(category=category), page, per_page, 'api.get_products_for_category', slug=slug)
    return jsonify(data)


@bp.route('/category/<category_slug>/product/<slug>')
def get_product(slug, category_slug):
    return jsonify(Product.query.filter_by(slug=slug).first().to_dict())
