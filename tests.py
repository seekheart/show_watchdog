from data_model.models import imdbInfo, db
from data_model.models import Episodes2Show as ep2show
import threading
from watchdog.watcher import Watcher

doggo = Watcher()

from time import clock

def timer(func):
	def wrapper(*args, **kwargs):
		start = clock()
		data = func(*args, **kwargs)
		print("Time taken for {}: is {:.6f}".format(func.__name__, clock() - start))
		return data
	return wrapper

@timer
def threaded_get_all_episodes():
	threads = []
	programs = {}
	#print(doggo.get_episodes(doggo.tracked_shows[0]))
	for show in doggo.tracked_shows:
		_thread = threading.Thread(target=doggo.episode_thread_worker, args=([show], programs))
		threads.append(_thread)
		_thread.start()

	for _thread in threads:
		_thread.join()
	return programs

@timer
def get_all_episodes():
	programs = {}
	for show in doggo.tracked_shows:
		programs[show['title']] = doggo.get_episodes(show)

	return programs

@timer
def get_titles_from_watcher():
	return doggo.get_show_titles()

@timer
def get_titles_from_db():
	return imdbInfo.Title.distinct()

a = get_titles_from_db()
b = get_titles_from_watcher()
#c = threaded_get_all_episodes()
#d = get_all_episodes()