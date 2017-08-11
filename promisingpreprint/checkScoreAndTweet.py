## Periodically query altmetric all entries in database younger than 1 week
## As soon as threshold (better than top 90% score journal) is passed, tweet about article
# Part of PromisingPreprint
# wdecoster

from altmetric import Altmetric
from os import path
from time import sleep
from datetime import datetime
from secrets import *
import tweepy
import logging
import logging.handlers
import argparse


def queryAltmetric(doi):
    '''
    Check the altmetric journal percentile score of the publication
    '''
    a = Altmetric()
    sleep(2)
    try:
        resp = a.doi(doi)
        if resp:
            return resp["context"]['journal']['pct'] # Percentage attention for this journal
        else:
            return 0
    except AltmetricHTTPException as e:
        if e.status_code == 403:
            logging.error("You aren't authorized for this call: {}".format(doi))
        elif e.status_code == 420:
            logging.error("You are being rate limited, currently {}".format(doi))
            sleep(60)
        elif e.status_code == 502:
            logging.error("The API version you are using is currently down for maintenance.")
        elif e.status_code == 404:
            logging.error("Invalid API function")
            print(e.msg)


def tweet(message, api, dry):
    '''
    Tweet the message to the api, except if dry = True, then just print
    '''
    if dry:
        print(message)
    else:
        api.update_status(message)
        sleep(2)


def cleandb(currentlist, alreadyTweeted, dbf):
    '''
    Using the stored list of entries check if the articles aren't older than 1 week
    Save only those younger than 1 week to same file (overwrite)
    Also remove those which were already tweeted
    '''
    currentTime = datetime.now()
    with open(dbf, 'w') as db_updated:
        for doi, link, title, date, status in currentlist:
            if (currentTime - datetime.strptime(date.strip(), "%Y-%m-%d")).days <= 7:
                if doi in alreadyTweeted:
                    db_updated.write("{}\t{}\t{}\t{}\t{}\n".format(doi, link, title, date, "tweeted"))
                else:
                    db_updated.write("{}\t{}\t{}\t{}\t{}\n".format(doi, link, title, date, "SeenNotTweeted"))


def readdb(dbf):
    '''
    Get all saved metrics from the database saved to file
    '''
    if path.isfile(dbf):
        with open(dbf, 'r') as db:
            return [i.strip().split('\t') for i in db]
    else:
        return []


def getArgs():
    parser = argparse.ArgumentParser(description="Checking altmetric score of preprints in database and tweet if above cutoff.")
    parser.add_argument("-d", "--dry", help="Print instead of tweeting", action="store_true")
    return parser.parse_args()


def setupTweeting():
    '''
    Setup the tweeting api using the keys and secrets imported from secrets.py
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)


def setupLogging():
    '''
    Setup a rotating log in which each file can maximally get 10kb
    5 backups are kept in addition to the current file
    '''
    logname = "/home/pi/projects/PromisingPreprint/checkScoreAndTweet.log"
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(logname, maxBytes=10000, backupCount=5)
    handler.setFormatter(logging.Formatter("{asctime} {levelname:8s} {message}", style='{'))
    my_logger.addHandler(handler)
    my_logger.info('Started.')

def main():
    try:
        args = getArgs()
        if args.dry:
            my_logger.info("Running in dry mode.")
        setupLogging()
        db="/home/pi/projects/PromisingPreprint/preprintdatabase.txt"
        api = setupTweeting()
        currentlist = readdb(db)
        tweeted = []
        for doi, link, title, date, status in currentlist:
            if status == 'tweeted':
                tweeted.append(doi)
                continue
            pct = queryAltmetric(doi)
            assert 0 <= pct <= 100
            if pct >= 90:
                tweet("{}\n{}".format(title, link), api, args.dry)
                tweeted.append(doi)
        cleandb(currentlist, tweeted, db)
        my_logger.info('Finished.\n')
    except Exception as e:
        my_logger.error(e, exc_info=True)
        raise


if __name__ == '__main__':
    main()
