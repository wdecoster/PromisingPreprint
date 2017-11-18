# Frequently check RSS, save results to database
# Part of PromisingPreprint
# wdecoster

import feedparser
from os import path
import logging
import logging.handlers
import pickle


class Preprint(object):
    def __init__(self, doi, url, title, date):
        self.doi = doi
        self.url = url
        self.title = title
        self.date = date


def checkRSS(preprints):
    '''
    Check the RSS feed of biorxiv and for each paper, save doi, link and title
    Except if the doi was already seen, then don't duplicate
    '''
    dois_seen = [p.doi for p in preprints]
    feed = feedparser.parse("http://connect.biorxiv.org/biorxiv_xml.php?subject=all")
    if 'bozo_exception' in feed.keys():
        pass
        my_logger.error("Failed to reach the feed")
    else:
        for pub in feed["items"]:
            if not pub['dc_identifier'] in dois_seen:
                my_logger.info("Adding article {} to database".format(pub['dc_identifier']))
                preprints.append(
                    Preprint(doi=pub['dc_identifier'],
                             url=trimlink(pub["link"]),
                             title=pub["title"],
                             date=pub['updated']))
        pickle.dump(
            obj=preprints,
            file=open(DATABASE, 'wb'))


def trimlink(url):
    """Remove unnessecary parts from the url."""
    return url.split('?')[0]


def load_database():
    """If database exists, return content."""
    if path.isfile(DATABASE):
        with open(DATABASE, 'rb') as db:
            return pickle.load(db)
    else:
        my_logger.warning("Unexpected: Database not found")
        return []


def setup_logging():
    '''
    Setup a rotating log in which each file can maximally get 10kb
    5 backups are kept in addition to the current file
    '''
    logname = "/home/pi/projects/PromisingPreprint/getPreprintsAndSave.log"
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(logname, maxBytes=10000, backupCount=5)
    handler.setFormatter(logging.Formatter("{asctime} {levelname:8s} {message}", style='{'))
    my_logger.addHandler(handler)
    my_logger.info('Started.')
    return my_logger


def main():
    try:
        db = load_database()
        checkRSS(db)
        # my_logger.info('Finished.\n')
    except Exception as e:
        my_logger.error(e, exc_info=True)
        raise


if __name__ == '__main__':
    DATABASE = "/home/pi/projects/PromisingPreprint/preprintdatabase.pickle"
    my_logger = setup_logging()
    main()
