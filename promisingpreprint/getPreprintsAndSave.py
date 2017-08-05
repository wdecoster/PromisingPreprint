# Frequently check RSS, save results to database
# Part of PromisingPreprint
# wdecoster

import feedparser
from os import path
import logging


def checkRSS(dois_seen, dbf):
    '''
    Check the RSS feed of biorxiv and for each paper, save doi, link and title
    Except if the doi was already seen, then don't duplicate
    '''
    feed = feedparser.parse("http://connect.biorxiv.org/biorxiv_xml.php?subject=all")
    if 'bozo_exception' in feed.keys():
        logging.error("Failed to reach the feed")
    else:
        for pub in feed["items"]:
            if not pub['dc_identifier'] in dois_seen:
                save2db(pub['dc_identifier'], pub["link"], pub["title"], pub['updated'], dbf)


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
        logging.warning("Unexpected: Database not found")
        return []


def main():
    try:
	db = "/home/pi/projects/PromisingPreprint/preprintdatabase.txt"
        logging.basicConfig(
                format='%(asctime)s %(message)s',
                filename="/home/pi/projects/PromisingPreprint/getPreprintsAndSave.log",
                level=logging.INFO)
        logging.info('Started.')
        dois_seen = readdb(db)
        checkRSS(dois_seen, db)
        logging.info('Finished.\n')
    except Exception as e:
        logging.error(e, exc_info=True)
        raise


if __name__ == '__main__':
    main()
