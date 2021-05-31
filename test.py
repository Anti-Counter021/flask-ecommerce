from datetime import date

import unittest

from app import create_app, db
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
from config import Config


class TestConfig(Config):
    """ Test config """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelTestCase(unittest.TestCase):
    """ User model tests """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.u = User(username='test', email='test@example.com')
        db.session.add(self.u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """ Password hashing """
        self.u.set_password('test')
        self.assertFalse(self.u.check_password('dog'))
        self.assertTrue(self.u.check_password('test'))

    def test_reset_password_token(self):
        token = self.u.get_reset_password_token()
        self.assertEqual(self.u, User.verify_reset_password_token(token))

    def test_user_permission(self):
        self.assertEqual(self.u.permission, 'user')
        self.u.permission = 'admin'
        db.session.commit()
        self.assertEqual(self.u.permission, 'admin')


class CategoryAndFeatureModelsTestCase(unittest.TestCase):
    """ Category and features model tests """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.category = Category(name='Smartphones', slug='smartphones')
        self.product = Product(title='Iphone 11 Pro Max', slug='iphone-11-pro-max', price=2000, category=self.category)
        self.category_feature = CategoryFeature(category=self.category, feature_name='Diagonal', unit='inch')
        self.product_feature = ProductFeature(product=self.product, feature=self.category_feature, value='6.5')
        db.session.add(self.category)
        db.session.add(self.product)
        db.session.add(self.category_feature)
        db.session.add(self.product_feature)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_category_products(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.category.products.count(), 1)

    def test_category_features(self):
        self.assertEqual(self.category.feature.first(), self.category_feature)
        self.assertEqual(self.category_feature.category, self.category)
        self.assertEqual(self.category.feature.count(), 1)
        self.assertEqual(self.category.feature.first().feature_name, self.category_feature.feature_name)
        self.assertEqual(self.category_feature.feature_products.count(), 1)
        self.assertEqual(self.category_feature.feature_products.first(), self.product_feature)
        self.assertEqual(self.product_feature.feature, self.category_feature)


class CartAndCartProductAndOrderModelsTestCase(unittest.TestCase):
    """ Cart and Cart products model tests """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.category = Category(name='Smartphones', slug='smartphones')
        self.product = Product(title='Iphone 12 Pro Max', slug='iphone-12-pro-max', price=2000, category=self.category)
        self.user = User(username='test', email='test@example.com')
        self.cart = Cart(owner=self.user)
        db.session.add(self.category)
        db.session.add(self.product)
        db.session.add(self.user)
        db.session.add(self.cart)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_cart_user(self):
        self.assertEqual(self.cart.owner, self.user)
        cart_product = CartProduct(product=self.product, user=self.user, cart=self.cart, final_price=self.product.price)
        db.session.add(cart_product)
        db.session.commit()
        self.assertEqual(self.user, cart_product.user)
        self.assertEqual(cart_product.product, self.product)
        self.assertEqual(self.cart.products.first(), cart_product)
        cart_product.qty = 2
        cart_product.final_price = cart_product.qty * self.product.price
        db.session.commit()
        self.assertEqual(cart_product.qty, 2)
        self.assertEqual(cart_product.final_price, self.product.price * 2)
        product = Product(title='Iphone 13 Pro Max', slug='iphone-13-pro-max', price=3000, category=self.category)
        cart_product2 = CartProduct(product=product, user=self.user, cart=self.cart, final_price=product.price)
        self.cart.products.append(cart_product2)
        db.session.add(product)
        db.session.add(cart_product2)
        db.session.commit()
        self.assertEqual(self.cart.products.count(), 2)
        self.assertEqual(self.user.cart_product.count(), 2)
        order = Order(user=self.user, first_name='Arkady', last_name='Counter', phone='88005553535', cart=self.cart,
                      address='Baker Street', buying_type='self', comment='Good!')
        db.session.add(order)
        self.cart.in_order = True
        db.session.commit()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.cart, self.cart)
        self.assertEqual(order.order_date, date.today())
        self.assertEqual(order.cart.products.count(), 2)
        self.assertEqual(self.user.order.first(), order)
        self.assertEqual(self.user.order.count(), 1)


class TestimonialsModelTestCase(unittest.TestCase):
    """ Testimonial model tests """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(username='test', email='test@example.com')
        self.testimonial = Testimonial(user=self.user, appraisal='excellent', comment='Very good ecommerce!')
        db.session.add(self.user)
        db.session.add(self.testimonial)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_testimonial(self):
        self.assertEqual(self.user.testimonial.first(), self.testimonial)
        self.assertEqual(self.user.testimonial.count(), 1)
        self.assertEqual(self.testimonial.user, self.user)


if __name__ == '__main__':
    unittest.main(verbosity=2)
