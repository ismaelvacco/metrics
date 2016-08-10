import redis
import logging
import ConfigParser
import os

import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"..")
CONFIG_DIR =  "%s/etc/" % (BASE_DIR)

config = ConfigParser.RawConfigParser()
config.read("%s/config.ini" % (CONFIG_DIR))

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
r = redis.StrictRedis(host=config.get('redis','hostname'), port=config.getint('redis','port'), db=config.getint('redis','index'))



def index_customer_id():
    for k in r.scan_iter("*"):
        payload = json.loads(r.get(k))
        if '_cvar' in payload.keys():
            custom_vars = json.loads(payload['_cvar'])

            # customer id
            if "1" in custom_vars.keys():
                key = custom_vars["1"][0]
                value = custom_vars["1"][1]

                print {key:value}


if __name__ == '__main__':
    index_customer_id()
