# Part of PromisingPreprint
# wdecoster

from os import path
import pickle
from time import sleep
from altmetric import Altmetric


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

    def query_altmetric(self):
        """Check the altmetric journal percentile score of the publication."""
        a = Altmetric()
        sleep(2)
        try:
            resp = a.doi(self.doi)
            if resp:
                pct = resp["context"]['journal']['pct']
                assert 0 <= pct <= 100
                return 0, pct
            else:
                return 0, 0
        except Altmetric.HTTPException as e:
            if e.status_code == 403:
                return 403, "You aren't authorized for this call"
            elif e.status_code == 420:
                sleep(60)
                return 420, "You are being rate limited"
            elif e.status_code == 502:
                return 502, "Down for maintenance."
            elif e.status_code == 404:
                return 404, "Invalid API function"
                print(e.msg)


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
