from flask import Flask
from app import create_app, db
from config import DevelopmentConfig
from models import Users, Location, Favorites, Reviews
from uuid import uuid4
from random import uniform


def init_db(db):
    """run to populate an empty db with working test data"""
    name = [str(uuid4()) for _ in range(3)]
    user1 = Users(name=name[0], email=f'{name[0]}@test.com')
    user2 = Users(name=name[1], email=f'{name[1]}@test.com')
    user3 = Users(name=name[2], email=f'{name[2]}@test.com')

    loc = [(uniform(-90, 90), uniform(-180, 180)) for _ in range(3)]
    loc1 = Location(name='test1', lat=loc[0][0], lon=loc[0][1])
    loc2 = Location(name='test2', lat=loc[1][0], lon=loc[1][1])
    loc3 = Location(name='test3', lat=loc[2][0], lon=loc[2][1])

    USERS = [user1, user2, user3]

    LOCATIONS = [loc1, loc2, loc3]

    for val in USERS+LOCATIONS:
        db.session.add(val)

    db.session.commit()

    fav1 = Favorites(user_id=user1.id, loc_id=loc1.id)
    fav2 = Favorites(user_id=user1.id, loc_id=loc2.id)
    fav3 = Favorites(user_id=user2.id, loc_id=loc1.id)

    rev1 = Reviews(user_id=user1.id, loc_id=loc1.id, comment='eh', review=3)
    rev2 = Reviews(user_id=user1.id, loc_id=loc2.id, comment='poor', review=2)
    rev3 = Reviews(user_id=user2.id, loc_id=loc1.id,
                   comment='rockin', review=5)

    REVIEWS = [rev1, rev2, rev3]
    FAVORITES = [fav1, fav2, fav3]

    for val in REVIEWS+FAVORITES:
        db.session.add(val)

    db.session.commit()


if __name__ == '__main__':
    app = create_app(DevelopmentConfig).app
    app.app_context().push()
    init_db(db)
