# Periodically query altmetric all entries in database younger than 1 month
# As soon as threshold (better than top 90% score journal) is passed, tweet about article
# Part of PromisingPreprint
# wdecoster


from datetime import datetime
import secrets
import tweepy
import argparse
from utils import setup_logging
from preprint import load_database, save_database
from altmetric import Altmetric
from time import sleep
from random import shuffle


def main():
    try:
        args = get_args()
        twitter_api = setup_tweeting()
        preprints = load_database()
        preprints = shuffle(preprints)
        altmetric_api = Altmetric(apikey=secrets.altmetric_key)
        for preprint in preprints:
            if preprint.status == 'tweeted':
                continue
            return_code, res = preprint.query_altmetric(altmetric_api)
            if return_code:
                my_logger.error(res)
            else:
                if res >= 90:
                    if not args.dry:
                        preprint.tweet(twitter_api)
                    else:
                        preprint.dry_print()
            sleep(3)
        clean_database(preprints)
        my_logger.info('Finished.\n')
    except Exception as e:
        my_logger.error(e, exc_info=True)
        print("Terminating...")
        clean_database(preprints)
        raise


def get_args():
    parser = argparse.ArgumentParser(
        description="Checking altmetric score of preprints in database and tweet if above cutoff.")
    parser.add_argument("-d", "--dry", help="Print instead of tweeting", action="store_true")
    args = parser.parse_args()
    if args.dry:
        my_logger.info("Running in dry mode.")
    return args


def setup_tweeting():
    """Setup the tweeting api using the keys and secrets imported from secrets.py"""
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_secret)
    return tweepy.API(auth)


def clean_database(preprints, days=31):
    """Remove preprints older than days"""
    currentTime = datetime.now()
    save_database([p for p in preprints if (
        currentTime - datetime.strptime(p.date, "%Y-%m-%d")).days <= days])


if __name__ == '__main__':
    my_logger = setup_logging("/home/pi/projects/PromisingPreprint/checkScoreAndTweet.log")
    main()
