import tornado.ioloop
import tornado.web

from toredis import Client

import json
import ConfigParser

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"..")
STATIC_DIR =  "%s/static/" % (BASE_DIR)
CONFIG_DIR =  "%s/etc/" % (BASE_DIR)

config = ConfigParser.RawConfigParser()
config.read("%s/config.ini" % (CONFIG_DIR))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        payload = json.dumps({ k: self.get_argument(k) for k in self.request.arguments })
        id = self.get_argument('_id')
        browsertime = "%02d%02d%02d%s" % (int(self.get_argument('h')), int(self.get_argument('m')), int(self.get_argument('s')), self.get_argument('r'))
        key = "transaction:%s:%s" % (id, browsertime)
        redis.set(key, payload)
        self.write("")

def make_app():
    return tornado.web.Application([
        (r"/capture", MainHandler),

        # serve pikik tag
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': STATIC_DIR}),
    ])

def set_database():
    redis.select(config.getint('redis','index'))


if __name__ == "__main__":
    app = make_app()
    app.listen(config.getint('server','port'))
    redis = Client()
    redis.connect(host=config.get('redis','hostname'), port=config.getint('redis','port'), callback=set_database)
    tornado.ioloop.IOLoop.current().start()