from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from app import db
from app.models import Category, Product, Cart, CartProduct
from app.cart_search import get_cart, recalculate_cart
from app.main import bp


@bp.route('/')
def index():
    """ Home """
    products = Product.query.all()
    return render_template('base.html', products=products, header=1)


@bp.route('/category/<slug>')
def category_detail(slug):
    """ Category Detail """
    category = Category.query.filter_by(slug=slug).first()
    return render_template('category_detail.html', category=category, title=f'Category - {category.name}')


@bp.route('/category/<category_slug>/products/<product_slug>')
def product_detail(category_slug, product_slug):
    """ Product detail """
    product = Product.query.filter_by(slug=product_slug).first()
    return render_template('product_detail.html', product=product, title=f'Product - {product.title}')


@bp.route('/cart')
def cart():
    """ Cart """
    return render_template('cart.html', title='Cart')


@bp.route('/cart/add/<slug>')
@login_required
def add_to_cart(slug):
    """ Add to cart """
    product = Product.query.filter_by(slug=slug).first()
    cart = get_cart()
    cart_product = CartProduct.query.filter_by(user=current_user, cart=cart, product=product).first()
    if not cart_product:
        cart_product = CartProduct(user=current_user, cart=cart, product=product)
        cart_product.final_price = product.price
        db.session.add(cart_product)
        cart.products.append(cart_product)
        db.session.commit()
    recalculate_cart(cart)
    flash('Product added.')
    return redirect(url_for('main.cart'))


@bp.route('/cart/change-qty/<slug>', methods=['GET', 'POST'])
@login_required
def change_qty(slug):
    """ Change quantity """
    cart = get_cart()
    product = Product.query.filter_by(slug=slug).first()
    cart_product = CartProduct.query.filter_by(user=current_user, cart=cart, product=product).first()
    qty = int(request.form['qty'])
    cart_product.qty = qty
    cart_product.final_price = product.price * qty
    db.session.commit()
    recalculate_cart(cart)
    flash('Quantity from product changed.')
    return redirect(url_for('main.cart'))
