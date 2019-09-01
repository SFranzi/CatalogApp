from app import app, db
from app.models import Category, Item, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'Item': Item, 'User': User}
