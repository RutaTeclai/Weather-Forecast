""" """

from flask import (Flask, render_template, request,
                    flash, session, redirect)
from model import db, User, Visit, Forecast_office, Forecast, connect_to_db
import server

import requests
import json

def forecast_request(office):
   
    office_id = office.forecast_office_id
    grid_x = int(office.grid_x)
    grid_y = int(office.grid_y)

    res = requests.get(f'https://api.weather.gov/gridpoints/{office_id}/{grid_x},{grid_y}/forecast')
    forecast = res.json()
    # print(forecast)
    # print(forecast['properties']['periods']) list of dictionaries of daily forecast

    return forecast


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

def show_forecast(city,state):

    coordinate_list = city_geodata(city,state)

    lat, lng = coordinate_list
    res = requests.get(f'https://api.weather.gov/points/{lat},{lng}')

    forecast_office = res.json()
    forecast_office_data = forecast_office['properties']
    res = requests.get(f'{forecast_office_data["forecast"]}')
    forecast = res.json()

    # res_office = requests.get(f'forecast["properties"]["GridId"]')
    # forecast['name']=res_office.json()['name']

    return forecast



    


    
        
