# Part of PromisingPreprint
# wdecoster

import logging.handlers
import logging
import os


def setup_logging(path):
    '''
    Setup a rotating log in which each file can maximally get 10kb
    5 backups are kept in addition to the current file
    '''
    if os.path.isfile(path):
        logfile = path
    else:
        logfile = "temporary.log"
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10000, backupCount=5)
    handler.setFormatter(logging.Formatter("{asctime} {levelname:8s} {message}", style='{'))
    my_logger.addHandler(handler)
    my_logger.info('Started.')
    return my_logger
