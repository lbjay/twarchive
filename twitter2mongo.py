
import sys
import urllib2
import urllib
import simplejson
import time
from os.path import dirname, abspath
from twarchive import *
from optparse import OptionParser
from pymongo import Connection
from uuid import uuid4

import logging

def init_logging(logfile, verbose=False, debug=False):
    logging.basicConfig(
        filename = logfile, 
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s'
    )
    log = logging.getLogger()
    if verbose:
        log.addHandler(logging.StreamHandler(sys.stdout))
    if debug:
        log.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(thread)d %(filename)s %(lineno)d %(message)s')
        for h in log.handlers:
            h.setFormatter(fmt)
    return log

if __name__ == '__main__':

    op = OptionParser()
    op.set_usage("usage: twitter2mongo.py [options] query [query, ...] ")
    op.add_option('--verbose', dest='verbose', action='store_true',
        help='write log output to stdout', default=False)
    op.add_option('--debug', dest='debug', action='store_true',
        help='include debugging info in log output', default=False)
    op.add_option('--logfile', dest='logfile', action='store',
        help='write to this logfile', 
        default='%s/twitter2mongo.log' % dirname(dirname(abspath(__file__))))
    opts, args = op.parse_args()

    log = init_logging(opts.logfile, verbose=opts.verbose, debug=opts.debug)

    # use 1st positional argument as the db name
    db = get_database(args[0])
    log.debug("Using database %s" % db.name)
    tweet_collection = get_collection(db, 'tweets')
    query_collection = get_collection(db, 'queries')

    for query in args:
        try:
            log.info("searching for: %s" % query)
            tweets, query_meta = basic_search(query)
        except:
            raise
        else:
            query_id = uuid4().hex
            query_meta['_id'] = query_id
            query_meta['timestamp'] = time.time()
            last_error = query_collection.update({'_id': query_id}, query_meta, upsert=True, safe=True)
            for tweet in tweets:
                # reuse tweet id as our unique id
                tweet_id = tweet['id']
                tweet['_id'] = tweet_id
                tweet['query_id'] = query_id
                tweet_collection.update({'_id': tweet_id}, tweet, upsert=True)
            log.info("Saved %d tweets" % len(tweets))

