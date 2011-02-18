
import re
from urllib2 import urlopen
from urllib import urlencode
from simplejson import load
from pymongo import Connection, errors

def get_database(db_name, create=True, **kwargs):
    mongo = Connection(**kwargs)
    db_name = re.sub('\s+', '_', db_name)
    if not create and db_name not in mongo.database_names():
        raise errors.InvalidName("database %s does not exists" % db_name)
    return mongo[db_name]

def get_collection(db, collection_name, create=True):
    if not create and collection_name not in db.collection_names():
        raise errors.InvalidName("collection %s does not exists" % collection_name)
    return db[collection_name]

def basic_search(query):
    u = urlopen('http://search.twitter.com/search.json?%s' % urlencode({'q': query}))
    resp = load(u)
    tweets = resp['results']
    del resp['results']
    return tweets, resp
        
