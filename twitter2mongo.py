
import sys
import urllib2
import urllib
import simplejson
import time
from twarchive import *
from optparse import OptionParser
from pymongo import Connection
from uuid import uuid4

if __name__ == '__main__':

    op = OptionParser()
    op.set_usage("usage: twitter2mongo.py [options] query [query, ...] ")
    op.add_option('--debug', dest='debug', action='store_true',
        help='include debugging info in log output', default=False)
    opts, args = op.parse_args()

    # use 1st positional argument as the db name
    db = get_database(args[0])
    print "Using database %s" % db.name
    tweet_collection = get_collection(db, 'tweets')
    query_collection = get_collection(db, 'queries')

    for query in args:
        try:
            print "searching for: %s" % query
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
            print "Saved %d tweets" % len(tweets)

