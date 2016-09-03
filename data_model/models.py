from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('setting.Config') 
db = SQLAlchemy(app)

class imdbInfo(db.Model):
    __tablename__ = "imdbInfo"

    TTid = db.Column(db.String(50),primary_key=True)
    Title = db.Column(db.String(100))
    PosterURL = db.Column(db.String(200))

    def __init__(self, TTid, Title, PosterURL):
        self.TTid = TTid
        self.Title = Title
        self.PosterURL = PosterURL
    def __repr__(self):
        return "<ID {}>".format(self.TTid)
    def __str__(self):
        return "{}, {}".format(self.TTid, self.Title)

class Episodes2Show(db.Model):
    __tablename__ = 'episodes2show'

    EP_ID = db.Column(db.String(50), primary_key=True)
    Episode_TItle = db.Column(db.String(200))
    Show_TItle = db.Column(db.String(160))
    Show_ID = db.Column(db.String(50))

    def __init__(self, EP_ID, Episode_TItle, Show_TItle, Show_ID):
        self.EP_ID = EP_ID
        self.Episode_TItle = Episode_TItle
        self.Show_Title = Show_Title
        self.Show_ID = Show_ID

    def __repr__(self):
        return "<ID {}>".format(self.EP_ID)
    def __str__(self):
        return "{}, {}".format(self.EP_ID, self.Episode_TItle)