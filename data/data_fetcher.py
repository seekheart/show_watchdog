#!/usr/bin/env python
"""
Data Fetcher
Mike Tung
"""

from watchdog import watcher
import csv
def main():
    imdb_watcher = watcher.Watcher()
    data = imdb_watcher.tracked_shows
    header = ['id', 'title', 'poster']
    print(len(data))

    with open('data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    main()