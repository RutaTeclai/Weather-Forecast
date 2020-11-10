"""CRUD operations."""

from model import db, User, Visit, Forecast_office, connect_to_db
from datetime import datetime


def create_user(fname, lname, email, password, city, state):
    """Create and return a new user."""

    user = User(fname=fname,lname=lname,
                email=email, password=password,
                city=city, state=state)

    db.session.add(user)
    db.session.commit()

    return user



def create_visit(user, forecast_office):
    """ Create and return a new visit """

    visit = Visit(user=user, forecast_office=forecast_office)

    db.session.add(visit)
    db.session.commit()


    return visit


def create_forecast_office(forecast_office_id, office_name):
    """ Create and return a new Forecast Office - Wfo """

    forecast_office = Forecast_office(forecast_office_id = forecast_office_id, office_name = office_name)

    db.session.add(forecast_office)
    db.session.commit()

    return forecast_office






if __name__ == '__main__':
    from server import app
    connect_to_db(app)