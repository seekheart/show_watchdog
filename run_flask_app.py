#!/usr/bin/env python

#import stuff
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_wtf import Form
from watchdog import watcher
import os
import urllib.parse
from models import db, imdbInfo

app = Flask(__name__)
doggie = watcher.Watcher()
images = []
for show in doggie.get_show_titles():
    cur_images = doggie.get_poster(show)[show]
    try:
        #print(show)
        images.append(cur_images)
    except Exception as e:
        #print(show, e)
        pass

if len(imdbInfo.query.all()) == 0:
    # our database is empty
    for i in doggie.tracked_shows:
        if len(i["poster"]) <= 120:
            dummy = imdbInfo(i["id"], i["title"], i["poster"])
            db.session.add(dummy)
    db.session.commit()

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/movies')
def movies():
    if request.method == 'GET':
        show_name = request.form['showName']
        email = request.form['email']
        return show_name, email

@app.route('/search', methods=["GET", "POST"])
def search():
    show_object = imdbInfo.query.filter_by(Title=request.values["q"]).first()
    if show_object is not None:
        return redirect(url_for('shows',id=show_object.TTid))
    else:
        abort(404)

@app.route('/shows/<string:id>')
def shows(id):
    show_object = imdbInfo.query.filter_by(TTid=id).first()
    if show_object is not None:
        return "<img src={}></img>".format(show_object.PosterURL)

# @app.route('/movies')
# def home_page():
#     images = os.path.join(os.path.dirname(__file__), 'static/images/')
#     img_fi = os.listdir(images)
#     img_fi = ['{}{}'.format(images, urllib.parse.quote(f)) for f in img_fi]
#     #img_fi = ['{}{}'.format(images, f) for f in img_fi]
#     return render_template('index.html', images=img_fi)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
