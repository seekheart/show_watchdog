#!/usr/bin/env python

#import stuff
from data_model.models import db
from data_model.models import imdbInfo
from flask import Flask
from flask import render_template, request
from flask import redirect, url_for, abort
from flask_wtf import Form
from fuzzywuzzy import fuzz
import os
import urllib.parse
from data_model.models import db, imdbInfo, Users
from authentication import custom_auth
import time
from setting import DevelopmentConfig
import urllib.parse
from watchdog import watcher


app = Flask(__name__)
app.config.from_object('setting.Config')

@app.route('/')
def home():
    if 'username' in request.cookies and 'secret' in request.cookies:
        my_query = Users.query.filter_by(Username=request.cookies['username']).first()
        if my_query is not None and my_query.Username == request.cookies['username'] and my_query.Secret == request.cookies['secret']:
            return render_template('homepage.html', username=my_query.Username)
    else:
        return render_template('homepage.html', username=None)

@app.route('/movies', methods=['GET','POST'])
def movies():
    if request.method == 'POST':
        show_name = request.form['showName']
        email = request.form['email']
        return '{}, {}'.format(show_name, email)
    return redirect(url_for('home'))

@app.route('/search', methods=["GET", "POST"])
def search():
    search_string = request.values['q'].strip()
    if search_string == '':
        return redirect(url_for('shows',
            id='+'.join(k[0] for k in db.session.query(imdbInfo.Title).all())))
    fuzzes = ((k[0], fuzz.partial_ratio(search_string, k[0])) for k in db.session.query(imdbInfo.Title).all())
    fuzzes = sorted(fuzzes, key=lambda x: x[1], reverse=True)
    filter_fuzzes = (fuzz for fuzz in fuzzes if fuzz[1] >= 60)
    param_str = '+'.join(name[0] for name in filter_fuzzes)
    if param_str:
        return redirect(url_for('shows',id=param_str))
    else:
        abort(404)

@app.route('/shows/')
def shows():
    shows = request.args.get('id').split('+')
    show_objects = (imdbInfo.query.filter_by(Title=k).first().TTid for k in shows)
    if show_objects:
        return render_template('index.html', 
                images=["../static/images/{}.jpg".format(k) for k in show_objects])

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", login_error=False, register_error=False)
    else:
        values = request.values
        my_query = Users.query.filter_by(Username=values["username"]).first()
        if my_query is not None:
            new_password_hash = custom_auth.sha256_hash(my_query.Salt+values["password"])
            if my_query.Salty_Hash == new_password_hash:
                response = make_response(redirect('/'))
                response.set_cookie('username', my_query.Username)
                response.set_cookie('secret', my_query.Secret)

                return response
            else:
                return render_template('login.html', login_error=True, register_error=False)
        else:
            return render_template('login.html', login_error=True, register_error=False)


@app.route('/register', methods=["POST"])
def register():
    values = request.values
    if Users.query.filter_by(Username=values["username"]).first() is None:
        new_salt = custom_auth.random_fixed_string()
        new_password_hash = custom_auth.sha256_hash(new_salt + values["password"])
        new_secret = custom_auth.random_fixed_string()
        new_email = values["email"]
        new_user = Users(values["username"], new_password_hash, new_salt, new_secret, new_email, int(time.time()))
        db.session.add(new_user)
        db.session.commit()

        response = make_response(redirect('/'))
        response.set_cookie('username', values['username'])
        response.set_cookie('secret', new_secret)
        return response
    else:
        return render_template('login.html', login_error=False, register_error=True)
if __name__ == '__main__':
    app.run(port=DevelopmentConfig.PORT,
            debug=DevelopmentConfig.DEBUG)
