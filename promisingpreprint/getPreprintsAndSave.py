# Frequently check RSS, save results to database
# Part of PromisingPreprint
# wdecoster

import feedparser
from preprint import Preprint, load_database, save_database
from utils import setup_logging


def check_RSS(preprints):
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
                             url=trim_link(pub["link"]),
                             title=pub["title"],
                             date=pub['updated'],
                             status="new"))
        save_database(preprints)


def trim_link(url):
    """Remove unnessecary parts from the url."""
    return url.split('?')[0]


def main():
    try:
        db = load_database()
        if not db:
            my_logger.warning("Unexpected: Database not found")
        check_RSS(db)
        my_logger.info('Finished.\n')
    except Exception as e:
        my_logger.error(e, exc_info=True)
        raise


if __name__ == '__main__':
    my_logger = setup_logging("/home/pi/projects/PromisingPreprint/getPreprintsAndSave.log")
    main()
