# Part of PromisingPreprint
# wdecoster

from os import path
import pickle
from time import sleep


class Preprint(object):
    def __init__(self, doi, url, title, date, status):
        self.doi = doi
        self.url = url
        self.title = title
        self.date = date
        self.status = status

    def tweet(self, api):
        """"Tweet the message to the api"""
        message = "{}\n{}".format(shorten(self.title), self.url)
        self.status = "tweeted"
        api.update_status(message)
        sleep(2)

    def dry_print(self):
        print("{}\n{}".format(shorten(self.title), self.url))


def shorten(s):
    """Shorten the title if necessary."""
    if len(s) < 110:
        return s
    else:
        return s[:110] + "..."


def load_database():
    """If database exists, return content."""
    if path.isfile(DATABASE):
        with open(DATABASE, 'rb') as db:
            return pickle.load(db)
    else:
        return []


def save_database(preprints):
    pickle.dump(
        obj=preprints,
        file=open(DATABASE, 'wb'))


#DATABASE = "/home/pi/projects/PromisingPreprint/preprintdatabase.pickle"
DATABASE = "preprintdatabase.pickle"
