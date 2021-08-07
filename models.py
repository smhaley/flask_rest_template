from logging import NullHandler
from datetime import datetime
from sqlalchemy.orm import backref
from app import db


class Location(db.Model):
    __tablename__ = 'location'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float(precision=5), nullable=False)
    lon = db.Column(db.Float(precision=5), nullable=False)
    description = db.Column(db.String, nullable=True)

    favorites = db.relationship('Favorites', backref='location')
    reviews = db.relationship('Reviews', backref='location')

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    favorites = db.relationship('Favorites', backref='user')
    reviews = db.relationship('Reviews', backref='user')

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Favorites(db.Model):
    __tablename__ = 'favorites'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Reviews(db.Model):
    __tablename__ = 'location_info'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    review = db.Column(db.Integer, nullable=False)

    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<id {}>'.format(self.id)
