# Frequently check RSS, save results to database
# Part of PromisingPreprint
# wdecoster

import feedparser
from os import path
import logging
import logging.handlers


def checkRSS(dois_seen, dbf):
    '''
    Check the RSS feed of biorxiv and for each paper, save doi, link and title
    Except if the doi was already seen, then don't duplicate
    '''
    feed = feedparser.parse("http://connect.biorxiv.org/biorxiv_xml.php?subject=all")
    if 'bozo_exception' in feed.keys():
        my_logger.error("Failed to reach the feed")
    else:
        for pub in feed["items"]:
            if not pub['dc_identifier'] in dois_seen:
                my_logger.info("Adding article {} to database".format(pub['dc_identifier']))
                save2db(pub['dc_identifier'], trimlink(pub["link"]), pub["title"], pub['updated'], dbf)

def trimlink(url):
    '''
    Remove unnessecary parts from the url
    '''
    return url.split('?')[0]


def save2db(doi, link, title, date, dbf):
    '''
    Save article metrics to the database
    Add status 'notTweeted', since this publication is new
    '''
    with open(dbf, 'a') as db:
        db.write("{}\t{}\t{}\t{}\t{}\n".format(doi, link, title, date, 'notTweeted'))


def readdb(dbf):
    '''
    Return all DOIs in the database file
    '''
    if path.isfile(dbf):
        with open(dbf, 'r') as db:
            return [i.split('\t')[0] for i in db]
    else:
        my_logger.warning("Unexpected: Database not found")
        return []

def setupLogging():
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
        db = "/home/pi/projects/PromisingPreprint/preprintdatabase.txt"
        dois_seen = readdb(db)
        checkRSS(dois_seen, db)
        my_logger.info('Finished.\n')
    except Exception as e:
        my_logger.error(e, exc_info=True)
        raise


if __name__ == '__main__':
    my_logger = setupLogging()
    main()
