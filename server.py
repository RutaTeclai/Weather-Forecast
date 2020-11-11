"""Server for weather forecasts app."""

from flask import (Flask, render_template, request,
                    flash, session, redirect, requests)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

import json


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    state_code = open('data/data.json').read()

    state_code_dict = json.loads(state_code)


    return render_template('homepage.html', state_code = state_code_dict)


@app.route('/create_user', methods=['POST'])
def create_user_account():
    """ Register a new User """

    fname= request.form.get('fname')
    lname= request.form.get('lname')
    email= request.form.get('email')
    password= request.form.get('password')
    city= request.form.get('city')
    state= request.form.get('state')

    user = crud.get_user_by_email(email)
    print(user)

    if user:
        flash("The email already in use. Use different email!")
        

    else:
        crud.create_user(fname, lname, email, password, city, state)
        flash("Account successful created. Please Log In")

    return redirect('/')


@app.route('/forecast')
def show_forecast_page():
    email= request.args.get('email')
    password= request.args.get('password')

    user= crud.get_user_by_email(email)
    if user:

        return render_template('forecastpage.html')
    else:
        flash("Enter correct email and password or create a new user account")
        return redirect('/')


def city_geodata(city_name,state):
    coordinates = []
    city_data = open('data/trial.json').read()

    city_data_dict = json.loads(city_data)
    for city in city_data_dict:
        
        if city['city'] == city_name and city['state_id'] == state:
            latitude = city['lat']
            longitude = city['lng']
            coordinates.extend([latitude,longitude])
            
    return (coordinates)

def get_forecast_office(coordinate_list):
    lat, lng = coordinate_list
    res = requests.get('https://api.weather.gov/points/44.7544,-93.3631')
    res = requsests.get(f'https://api.weather.gov/points/{lat},{lng}')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
