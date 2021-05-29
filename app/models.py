from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Category(db.Model):
    """ Category """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    slug = db.Column(db.String(128), index=True, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """ Product """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    slug = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer, index=True, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    cart_product_id = db.relationship('CartProduct', backref='product', lazy='dynamic')

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


class CartProduct(db.Model):
    """ Cart product """
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qty = db.Column(db.Integer, default=1)
    final_price = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<CartProduct {self.id}>'


class Cart(db.Model):
    """ Cart """
    id = db.Column(db.Integer, primary_key=True)
    products_id = db.relationship('CartProduct', backref='cart', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_products = db.Column(db.Integer, default=0)
    final_price = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Cart {self.id}>'


@login.user_loader
def load_user(id):
    """ Loading user """
    return User.query.get(int(id))
