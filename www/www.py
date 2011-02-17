
import sys
import os
from os.path import dirname, abspath
os.environ['PYTHON_EGG_CACHE'] = dirname(abspath(__file__)) + '/.egg-cache'

import web
from web.webapi import badrequest, header, NotFound
import pymongo
from simplejson import dumps

urls = (
    '/user/([\w]+)$', 'User',
)

class User:
    def GET(self, username):
        mongo = pymongo.Connection()
        db = mongo[username]
        coll = db['tweets']
        tweets = []
        for t in coll.find({}):
            del t['_id']
            tweets.append(t)
        header('Content-type', 'application/json; charset=utf-8')
        return dumps(tweets)

app = web.application(urls, globals())
application = app.wsgifunc()

