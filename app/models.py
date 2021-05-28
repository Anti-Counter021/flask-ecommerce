from app import db


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

    def __repr__(self):
        return f'<Product {self.title}>'
