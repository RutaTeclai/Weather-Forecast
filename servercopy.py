"""Server for weather forecasts app."""

from flask import (Flask, render_template, request,
                    flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

import json
import requests


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
        user_city = user[0].city
        user_state = user[0].state 
        user_coordinates = city_geodata(user_city, user_state)
        user_forecast_dict = get_forecast_office_dict(user_coordinates)
        forecast_url = user_forecast_dict['forecast']
        res4 = requests.get(forecast_url)
        forecast_dict = res4.json()
        print(forecast_dict)

        # res4 = requests.get('forecast_dict')
        # print(res4.json())
        forecasts = []
        return render_template('forecastpage.html', user_city = user_city, 
                                user_state = user_state,
                                user_forecast_dict= user_forecast_dict,
                                forecast_dict = forecast_dict,forecasts=forecasts)
    else:
        flash("Enter correct email and password or create a new user account")
        return redirect('/')


def city_geodata(city_name,state):
    coordinates = []
    city_data = open('data/cities_geodata.json').read()

    city_data_dict = json.loads(city_data)
    for city in city_data_dict:
        
        if city['city'] == city_name and city['state_id'] == state:
            latitude = city['lat']
            longitude = city['lng']
            coordinates.extend([latitude,longitude])
            
    return coordinates

def get_forecast_office_dict(coordinate_list):
    lat, lng = coordinate_list
    res = requests.get(f'https://api.weather.gov/points/{lat},{lng}')

    forecast_office = res.json()
    forecast_office_data = forecast_office['properties']
    res1 = requests.get(f'https://api.weather.gov/offices/{forecast_office_data["cwa"]}')
    forecast_office_data['office_name'] = res1.json()['name']
    res2 = requests.get(forecast_office_data['observationStations'])
    # print((res2.json()['features'])[0]['properties']['name'])
    forecast_office_data['station'] = (res2.json()['features'])[0]['properties']['name']
    # print(forecast_office_data['observationStations'].properties)
    # print(forecast_office_data)
    return forecast_office_data
    # return forecast_office_data['cwa']
    # top_office = crud.create_forecast_office(forecast_office_data['cwa'], 'Topeka,KS' , forecast_office_data['gridX'], forecast_office_data['gridY'])
    

    # return forecast_office_data
    # forecast_office_id = forecast_office_data['cwa']
    # forecast_office_data['gridX']
    # forecast_office_data['gridY']




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
