from app import app, db
from app.models import Item, Category 

c1 = Category(title='Soccer')
c2 = Category(title='Basketball')
c3 = Category(title='Baseball')
c4 = Category(title='Frisbee')
c5 = Category(title='Snowboarding')
db.session.add_all([c1, c2, c3, c4, c5])
db.session.commit()

i1 = Item(title='Snowboard', description='This is the description', category=c5)
i2 = Item(title='Googles', description='This is the description', category=c5)
i3 = Item(title='Two Shinguards', description='This is the description', category=c1)
i4 = Item(title='Frisbee', description='This is the description', category=c4)
i5 = Item(title='Basketball', description='This is the description', category=c2)
i6 = Item(title='Bat', description='This is the description', category=c3)
db.session.add_all([i1, i2, i3, i4, i5, i6])
db.session.commit()




