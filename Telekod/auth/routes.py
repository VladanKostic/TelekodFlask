from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from localStoragePy import localStorage
from Telekod.auth.froms import LoginForm
from Telekod.auth.__utils__ import is_logged_in
import requests
import json


auth = Blueprint("auth", __name__, template_folder='auth')


# Home page
@auth.route('/')
def home():
    return redirect(url_for('login'))


# Authorisation
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print(form.validate())
    if request.method == "POST" and form.validate():
        # Get Form Fields
        email = request.form['email']
        password = request.form['password']
        pin = request.form['pin']
        authentication = {'email': email, 'password': password, 'pin': pin}
        r = requests.post('https://reqres.in/api/login', json=authentication)
        mylocalstorage = localStorage('qwert')
        y = json.loads(r.text)
        mylocalstorage.setItem("token", y["token"])
        session['logged_in'] = True
        session['user'] = email
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)


# User logout
@auth.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('auth.login'))
