#!/usr/bin/env python
"""
Imdb Utilities
Mike Tung
"""

#imports
from watcher import Watcher
from data_model.models import db
from data_model.models import imdbInfo
from data_model.models import Episodes2Show

def bootstrap_db():
    """
    function to load data into db
    """

    doggie = Watcher()
    db.create_all()
    shows = doggie.tracked_shows

    for show in shows:
        row = imdbInfo(show['id'], show['title'], show['poster'])
        db.session.add(row)
    db.session.commit()
    eps = a.get_all_episodes()

    for record in shows:
        eps = all_eps[record['title']]
        for e in eps:
            try:
                row = Episodes2Show(e.imdb_id, 
                                    e.title, 
                                    record['title'],
                                    record['id'])
            except json.decoder.JSONDecodeError as e:
                print(e)
            db.session.add(row)
        db.session.commit()