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
from setting import DevelopmentConfig
import urllib.parse
from watchdog import watcher

app = Flask(__name__)
app.config.from_object('setting.Config')

@app.route('/')
def home():
    return render_template('homepage.html')

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
            id='+'.join(k.Title for k in imdbInfo.query.all())))
    fuzzes = ((k.Title, fuzz.partial_ratio(search_string, k.Title)) for k in imdbInfo.query.all())
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

if __name__ == '__main__':
    app.run(port=DevelopmentConfig.PORT,
            debug=DevelopmentConfig.DEBUG)
