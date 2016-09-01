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
    #show_object = imdbInfo.query.filter(imdbInfo.Title.like("%{}%".format(request.values['q']))).first_or_404()
    fuzzes = list((k, fuzz.partial_ratio(request.values['q'], k)) for k in doggie.get_show_titles())
    fuzzes = sorted(fuzzes, key=lambda x: x[1], reverse=True)
    #print(fuzzes[:3])
    filter_fuzzes = list(fuzz for fuzz in fuzzes if fuzz[1] >= 60)
    if filter_fuzzes:
        return redirect(url_for('shows',id='+'.join(name[0] for name in filter_fuzzes)))
    else:
        abort(404)

@app.route('/shows/')
def shows():
    shows = request.args.get('id').split('+')
    show_objects = list(imdbInfo.query.filter_by(Title=k).first().TTid for k in shows)
    #print(show_objects)
    if show_objects:
        #return '<img src="../static/images/{}.jpg"></img>'.format(show_object.TTid)
        return render_template('index.html', 
                images=["../static/images/{}.jpg".format(k) for k in show_objects])

# @app.route('/movies')
# def home_page():
#     images = os.path.join(os.path.dirname(__file__), 'static/images/')
#     img_fi = os.listdir(images)
#     img_fi = ['{}{}'.format(images, urllib.parse.quote(f)) for f in img_fi]
#     #img_fi = ['{}{}'.format(images, f) for f in img_fi]
#     return render_template('index.html', images=img_fi)

if __name__ == '__main__':
    app.run(port=DevelopmentConfig.PORT, debug=DevelopmentConfig.DEBUG)
