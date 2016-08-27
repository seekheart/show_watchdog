#!/usr/bin/env python
"""
Imdb Watcher
Mike Tung
"""

import os
import string
import urllib.request
import urllib

from imdbpie import Imdb


class Watcher:
    def __init__(self):
        self.imdb = Imdb(anonymize=True)
        self.tracked_shows = self.get_shows()
        self.static_dir = os.path.join(os.path.dirname(__file__), '../static/images')

    def get_shows(self):
        """
        gets all current popular shows from imdb
        """
        shows = self.imdb.popular_shows()
        tracked_shows = []
        for show in shows:
            tracked_shows_d = {}
            tracked_shows_d['id'] = show['tconst']
            tracked_shows_d['title'] = show['title']
            tracked_shows_d['poster'] = show['image']['url']
            tracked_shows.append(tracked_shows_d)
        return tracked_shows

    def get_show_id(self, show_title):
        """
        Gets show title id

        args:

        show_title: name of show to be queried

        returns:

        show_id: id of show
        """

        for show in self.tracked_shows:
            if show_title == show['title']:
                return show['id']

    def get_episodes(self, show_id):
        """
        Gets all episodes of a given show

        args:

        show_id: tconst id from imdb

        returns:

        ist of episodes
        """
        return self.imdb.get_episodes(show_id)

    def get_all_episodes(self):
        """
        Gets all episodes

        args:

        None

        returns:

        list of episodes for all shows"""

        programs = {}
        for show in self.tracked_shows:
            programs[show['title']] = self.get_episodes(show['id'])

        return programs

    def get_poster(self, show_title):
        """
        gets the img url for the poster of a show

        args:

        show_title: title of show

        returns:

        dictionary with {show_title: poster_url}
        """

        #print(self.tracked_shows[show_id]['poster'])
        for show in self.tracked_shows:
            if show['title'] == show_title:
                return {show_title : show['poster']}

    def save_posters(self, urls, title):
        title = self.sanitize_title(title)
        dest = '{}/{}.jpg'.format(self.static_dir, title)
        urllib.request.urlretrieve(url, dest)

    def sanitize_title(self, title):
        forbidden = string.punctuation
        for char in forbidden:
            title = title.replace(char, '')
        return title

    def get_show_titles(self):
        """
        Gets show titles

        args:

        None

        returns:

        list of show titles
        """

        return [show['title'] for show in self.tracked_shows]

if __name__ == '__main__':
    a = Watcher()
    titles = a.get_show_titles()
    for t in titles:
        posters_dict = a.get_poster(t)
        for title, url in posters_dict.items():
            a.save_posters(url, title)
