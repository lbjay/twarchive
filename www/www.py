
import sys
import os
import site
from os.path import dirname, abspath
os.environ['PYTHON_EGG_CACHE'] = dirname(abspath(__file__)) + '/.egg-cache'
site.addsitedir(dirname(dirname(abspath(__file__))))

import web
from web.webapi import badrequest, header, NotFound
import pymongo
from simplejson import dumps
from twarchive import *

urls = (
    '/tweets/([\w]+)$', 'Tweets',
    '/queries/([\w]+)$', 'Queries',
)

class Tweets:
    def GET(self, dbname):
        db = get_database(dbname)
        collection = get_collection(db, 'tweets')
        tweets = list(collection.find({}))
        header('Content-type', 'application/json; charset=utf-8')
        return dumps(tweets)

class Queries:
    def GET(self, dbname):
        db = get_database(dbname)
        collection = get_collection(db, 'queries')
        queries = list(collection.find({}))
        header('Content-type', 'application/json; charset=utf-8')
        return dumps(queries)

app = web.application(urls, globals())
application = app.wsgifunc()

