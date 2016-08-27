from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms import validators, ValidationError

class ShowForm(Form):
    show_name = TextField('Show Name', [validators.Required("Please enter a show name")])
    email = TextField('Email', [validators.Required("Please enter an email")])
    submit = SubmitFIeld('Submit')