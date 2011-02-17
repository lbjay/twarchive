
import sys
import urllib2
import urllib
import simplejson
from optparse import OptionParser
from pymongo import Connection

if __name__ == '__main__':

    op = OptionParser()
    op.set_usage("usage: twitter2mongo.py [options] username ")
    op.add_option('--debug', dest='debug', action='store_true',
        help='include debugging info in log output', default=False)
    opts, args = op.parse_args()

    username = args[0]
    mongo = Connection()
    db = mongo[username]
    coll = db['tweets']
    coll.ensure_index('id', unique=True)

    u = urllib2.urlopen('http://search.twitter.com/search.json?%s' % urllib.urlencode({'q': username}))
    json = simplejson.load(u)

    for tweet in json['results']:
        coll.update({'id': tweet['id']}, tweet, upsert=True)
