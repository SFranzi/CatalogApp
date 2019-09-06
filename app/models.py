from app import db, login
from flask_login import UserMixin

# The Category class inherits from db.Model, a base class for
# all models from Flask-SQLAlchemy


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    # The backref argument defines the name of a field that will be added to
    # the objects of the "many" class that points back at the "one" object.
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.title)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        item = Item.query.filter_by(category_id=self.id).first()
        return {
            'id': self.id,
            'title': self.title
            }


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
    user_id = db.Column(db.String(64))
    #user_id = db.Column(db.String(), db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Item {}>'.format(self.title)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id
        }


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    #items = db.relationship('Item', backref='user', lazy='dynamic')


@login.user_loader
def load_user(id):
    return User.query.get(id)
