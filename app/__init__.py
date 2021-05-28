from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    """ Create app """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    bootstrap.init_app(app)

    from app.models import Product, Category
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models
