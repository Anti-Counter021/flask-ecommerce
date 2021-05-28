from app import create_app, db
from app.models import Category, Product

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'Product': Product}
