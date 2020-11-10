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
   

    def __repr__(self):
        """ show info about user """
        return f'<User user_id={self.user_id} email={self.email} city={self.city}, state={self.state}>'


class Visit(db.Model):
    """ A Forecast office Visit """

    __tablename__ = 'visits'

    visit_id = db.Column(db.Integer, 
                autoincrement=True,
                primary_key= True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    forecast_office_id = db.Column(db.String, db.ForeignKey('forecast_offices.forecast_office_id'))

    user = db.relationship('User')
    forecast_office = db.relationship('Forecast_office')


    def __repr__(self):
        return f'<Visit user_id={self.user_id}>'



class Forecast_office(db.Model):
    """ A Weather Forecast office - Wfo """

    __tablename__ = 'forecast_offices'

    forecast_office_id = db.Column(db.String, 
                                     primary_key= True)
    office_name = db.Column(db.String, nullable = False)


    visit = db.relationship('Visit')


    def __repr__(self):
        return f'<Forecast Office forecast_office_id={self.forecast_office_id} Forecast Office= {self.office_name}>'


class Station(db.Model):
    """ A Weather Forecast Observation Station """

    __tablename__ = 'stations'

    station_id = db.Column(db.String,
                            primary_key = True)
    station_name = db.Column(db.String, nullable = False)
    elevation = db.Column(db.Float, nullable = True)
    timezone = db.Column(db.String, nullable=True)

    forecast_office_id = db.Column(db.String, db.ForeignKey('forecast_offices.forecast_office_id'))

    def __repr__(self):
        return f'<Forecast Station station_id={self.station_id} Station Name= {self.station_name}>'


def connect_to_db(flask_app, db_uri='postgresql:///forecasts', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)
    
    
    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
