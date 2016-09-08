#!/usr/bin/env python

#import stuff
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_wtf import Form
from watchdog import watcher
import os
import urllib.parse
from data_model.models import db, imdbInfo
from setting import DevelopmentConfig
from fuzzywuzzy import fuzz

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

if __name__ == '__main__':
    app.run(port=DevelopmentConfig.PORT, debug=DevelopmentConfig.DEBUG)
