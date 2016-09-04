#!/usr/bin/env python
"""
Imdb Watcher
Mike Tung
"""

from imdbpie import Imdb
from imdbpie.objects import Episode
import os
import urllib.request
import urllib
import threading

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

    def get_episodes(self, show):
        """
        Gets all episodes of a given show

        args:

        show: show dictionary (or a dictionary with 'id' and 'title' keys)

        returns:

        list of episodes
        """

        if self.imdb.exclude_episodes:
            raise ValueError('exclude_episodes is currently set')

        url = self.imdb._build_url('/title/episodes', {'tconst': show['id']})
        response = self.imdb._get(url)

        if response is None:
            return None

        seasons = response.get('data').get('seasons')
        episodes = []

        for season in seasons:
            season_number = season.get('token')
            for idx, episode_data in enumerate(season.get('list')):
                episode_data['series_name'] = show['title']
                episode_data['episode'] = idx + 1
                episode_data['season'] = season_number
                episodes.append(Episode(episode_data))

        return episodes

    def episode_thread_worker(self, shows, programs):
        for show in shows:
            data = self.get_episodes(show)
            programs[show['id']] = data

    def get_all_episodes(self):
        """
        Gets all episodes

        args:

        None

        returns:

        list of episodes for all shows
        """
        threads = []
        programs = {}
        for show in self.tracked_shows:
            _thread = threading.Thread(target=self.episode_thread_worker, args=([show], programs))
            threads.append(_thread)
            _thread.start()

        for _thread in threads:
            _thread.join()

        return programs

    def save_posters(self, url, ttid):
        """saves posters as images in static/images"""
        dest = '{}/{}.jpg'.format(self.static_dir, ttid)
        print('Saving {}'.format(ttid))
        urllib.request.urlretrieve(url, dest)

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
    counter = 0
    # for record in a.tracked_shows:
    #     a.save_posters(record['poster'], record['id'])
    #     counter += 1
    #     print('Saved {} files'.format(counter))

    all_eps = a.get_all_episodes()
    header = ['Episode ID', 'Episode Title', 
                        'Show Title', 'Show ID', '\n']
    with open('show_eps.tsv', 'w') as outfile:
        outfile.write('\t'.join(header))
        for record in a.tracked_shows:
            eps = all_eps[record['title']]
            for e in eps:
                try:
                    line = [e.imdb_id, e.title, 
                                record['title'], record['id'], '\n']
                    line = [str(item) for item in line]
                    outfile.write('\t'.join(line))
                except json.decoder.JSONDecodeError as e:
                    print(e)