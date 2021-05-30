from datetime import datetime

from flask import current_app
from flask_login import UserMixin

import jwt

from time import time

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Category(db.Model):
    """ Category """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    slug = db.Column(db.String(128), index=True, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')
    feature = db.relationship('CategoryFeature', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """ Product """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    slug = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer, index=True, default=0)
    image_path = db.Column(db.String(350))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    cart_product_id = db.relationship('CartProduct', backref='product', lazy='dynamic')
    feature_id = db.relationship('ProductFeature', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.title}>'


class User(UserMixin, db.Model):
    """ User """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cart_product = db.relationship('CartProduct', backref='user', lazy='dynamic')
    cart_id = db.relationship('Cart', backref='owner', lazy='dynamic')
    order = db.relationship('Order', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """ Set password """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Check password """
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        """ Reset password token """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        """ Verify reset password token """
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class CartProduct(db.Model):
    """ Cart product """
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qty = db.Column(db.Integer, default=1)
    final_price = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CartProduct {self.id} - {self.product.title} - {self.user.username}>'


class Cart(db.Model):
    """ Cart """
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('CartProduct', backref='cart', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_products = db.Column(db.Integer, default=0)
    final_price = db.Column(db.Integer, default=0)
    for_anonymous_user = db.Column(db.Boolean, default=False)
    in_order = db.Column(db.Boolean, default=False)
    order = db.relationship('Order', backref='cart', lazy='dynamic')

    def __repr__(self):
        return f'<Cart {self.id} - {self.owner}>'


class Order(db.Model):
    """ Order """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    address = db.Column(db.String(255))
    buying_type = db.Column(db.String(10))
    comment = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    order_date = db.Column(db.Date, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id} - cart {self.cart.id} - {self.user.username}>'


class CategoryFeature(db.Model):
    """ Category Feature """
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    feature_name = db.Column(db.String(255))
    unit = db.Column(db.String(50))
    feature_products = db.relationship('ProductFeature', backref='feature', lazy='dynamic')

    def __repr__(self):
        return f'<Feature {self.feature_name} {self.unit} - {self.category.name}>'


class ProductFeature(db.Model):
    """ Product Feature """
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    feature_id = db.Column(db.Integer, db.ForeignKey('category_feature.id'))
    value = db.Column(db.String(255))

    def __repr__(self):
        return f'<Feature {self.feature.feature_name} {self.value} {self.feature.unit} - {self.product.title}>'


@login.user_loader
def load_user(id):
    """ Loading user """
    return User.query.get(int(id))
