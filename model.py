""" Models for weather forecasts app. """


from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(30), nullable = False)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    visit = db.relationship('Visit')
    rating = db.relationship('Rating')


    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} city={self.city}, state={self.state}>'