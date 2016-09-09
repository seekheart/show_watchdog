#!/usr/bin/env python

#import stuff
from flask import Flask, render_template, request, redirect, url_for, abort, make_response
from flask_wtf import Form
from watchdog import watcher
import os
import urllib.parse
from data_model.models import db, imdbInfo, Users
from setting import DevelopmentConfig
from fuzzywuzzy import fuzz
from authentication import custom_auth
import time

app = Flask(__name__)
app.config.from_object('setting.Config')
doggie = watcher.Watcher()

if len(imdbInfo.query.all()) == 0:
    # populate empty table
    for i in doggie.tracked_shows:
        dummy = imdbInfo(i["id"], i["title"], i["poster"])
        db.session.add(dummy)
    db.session.commit()

@app.route('/')
def home():
    if 'username' in request.cookies and 'secret' in request.cookies:
        my_query = Users.query.filter_by(Username=request.cookies['username']).first()
        if my_query is not None and my_query.Username == request.cookies['username'] and my_query.Secret == request.cookies['secret']:
            return render_template('homepage.html', username=my_query.Username)
    else:
        # TODO: handle false logins
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
        return redirect(url_for('shows', id='+'.join(k for k in doggie.get_show_titles())))
    #show_object = imdbInfo.query.filter(imdbInfo.Title.like("%{}%".format(request.values['q']))).first_or_404()
    fuzzes = ((k, fuzz.partial_ratio(search_string, k)) for k in doggie.get_show_titles())
    fuzzes = sorted(fuzzes, key=lambda x: x[1], reverse=True)
    #print(fuzzes[:3])
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
    #print(show_objects)
    if show_objects:
        return render_template('index.html', 
                images=["../static/images/{}.jpg".format(k) for k in show_objects])

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
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
                abort(404)
        # TODO (sam): properly handle wrong logins 
        else:
            abort(404)

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
        # TODO (sam): properly handle if user already exists
        abort(404)

if __name__ == '__main__':
    app.run(port=DevelopmentConfig.PORT, debug=DevelopmentConfig.DEBUG)
