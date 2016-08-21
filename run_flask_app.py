#!/usr/bin/env python

from flask import Flask, render_template
from watchdog import watcher
import os
import urllib.parse

app = Flask(__name__)

@app.route('/')
def home_page():
    images = os.path.join(os.path.dirname(__file__), 'static/images/')
    img_fi = os.listdir(images)
    img_fi = ['{}{}'.format(images, urllib.parse.quote(f)) for f in img_fi]
    return render_template('index.html', images=img_fi)

if __name__ == '__main__':
    app.run(port=3000, debug=True)