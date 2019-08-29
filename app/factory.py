from app import app, db
from app.models import Item, Category


def category_query():
    return Category.query
