#!/usr/bin/env python
"""
Imdb Utilities
Mike Tung
"""

#imports
from watchdog.watcher import Watcher
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

    if len(imdbInfo.query.all()) != 0:
        for show in shows:
            row = imdbInfo(show['id'], show['title'], show['poster'])
            db.session.add(row)
        db.session.commit()
    
    all_eps = doggie.get_all_episodes()

    if len(Episodes2Show.query.all()) != 0:
        for record in shows:
            eps = all_eps[record['id']]
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

if __name__ == '__main__':
    bootstrap_db()