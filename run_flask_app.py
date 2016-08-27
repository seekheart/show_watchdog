#!/usr/bin/env python

from flask import Flask, render_template
from watchdog import watcher
import os
import urllib.parse

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

@app.route('/')
def home_page():
    images = os.path.join(os.path.dirname(__file__), 'static/images/')
    img_fi = os.listdir(images)
    img_fi = ['{}{}'.format(images, urllib.parse.quote(f)) for f in img_fi]
    #img_fi = ['{}{}'.format(images, f) for f in img_fi]
    return render_template('index.html', images=img_fi)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
