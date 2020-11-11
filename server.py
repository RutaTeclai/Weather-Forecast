"""Server for weather forecasts app."""

from flask import (Flask, render_template, request,
                    flash, session, redirect)
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
    print(email)
    password= request.form.get('password')
    city= request.form.get('city')
    state= request.form.get('state')

    user = crud.get_user_by_email(email)
    print(user)

    if user:
        print('entering')
        flash("The email already in use. Use different email!")

    else:
        crud.create_user(fname, lname, email, password, city, state)
        flash("Account successful created. Please Log In")

    return redirect('/')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
