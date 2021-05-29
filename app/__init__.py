from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    """ Create app """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    admin.init_app(app)
    bootstrap.init_app(app)

    from app.models import Product, Category, User, CartProduct, Cart
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(CartProduct, db.session))
    admin.add_view(ModelView(Cart, db.session))

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models
