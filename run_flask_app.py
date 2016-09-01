#!/usr/bin/env python

#import stuff
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_wtf import Form
from watchdog import watcher
import os
import urllib.parse
from data_model.models import db, imdbInfo
from setting import DevelopmentConfig

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
    show_object = imdbInfo.query.filter(imdbInfo.Title.like("%{}%".format(request.values['q']))).first_or_404()
    if show_object is not None:
        return redirect(url_for('shows',id=show_object.TTid))
    else:
        abort(404)

@app.route('/shows/<string:id>')
def shows(id):
    show_object = imdbInfo.query.filter_by(TTid=id).first()
    if show_object is not None:
        return '<img src="../static/images/{}.jpg"></img>'.format(show_object.TTid)

# @app.route('/movies')
# def home_page():
#     images = os.path.join(os.path.dirname(__file__), 'static/images/')
#     img_fi = os.listdir(images)
#     img_fi = ['{}{}'.format(images, urllib.parse.quote(f)) for f in img_fi]
#     #img_fi = ['{}{}'.format(images, f) for f in img_fi]
#     return render_template('index.html', images=img_fi)

if __name__ == '__main__':
    app.run(port=DevelopmentConfig.PORT, debug=DevelopmentConfig.DEBUG)
