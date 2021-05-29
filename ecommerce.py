from app import create_app, db
from app.models import Category, Product, User

app = create_app()


@app.context_processor
def categories():
    return {'categories': Category.query.all()}


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'Product': Product, 'User': User}
