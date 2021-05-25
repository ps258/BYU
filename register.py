from tyk.decorators import *
from gateway import TykGateway as tyk
import jwt
#import redis
#from datetime import timedelta, datetime
import datetime
#from time import time
#from pprint import pprint

@Hook
def ResponseHook(request, response, session, metadata, spec):
  logLevel = "info"
  tyk.log("ResponseHook START", logLevel)
  tokenLife = 1*60
  private_key = open('/opt/tyk-certificates/gateway-key.pem').read()
  #r = redis.Redis(host="localhost",db=1)
  # show all the data structures
  #tyk.log("ResponseHook request object: " + str(vars(request)), logLevel)
  #tyk.log("ResponseHook response object: " + str(response), logLevel)
  #tyk.log("ResponseHook session object: " + str(session), logLevel)
  #tyk.log("ResponseHook metadata object: " + str(metadata), logLevel)
  #tyk.log("ResponseHook spec object: " + str(spec), logLevel)
  #tyk.log("ResponseHook: upstream returned {0}".format(response.status_code), logLevel)
  # Attach a new response header:
  token = response.raw_body.decode()
  #jot = jwt.encode({'scope': 'universal', 'sub': 'sub', 'client_id': 'mobile_apps', 'token': token, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=tokenLife), "iat": datetime.datetime.utcnow()}, "FredPassword")
  jot = jwt.encode({'scope': 'universal', 'sub': 'sub', 'client_id': 'mobile_apps', 'token': token, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=tokenLife), "iat": datetime.datetime.utcnow()}, private_key, algorithm='RS256')
  #r.setex(response.raw_body, timedelta(minutes=1), value="Fred was here")
  tyk.store_data(token, jot, tokenLife)
  tyk.log("ResponseHook: from redis " + tyk.get_data(token).decode(), logLevel)
  response.headers["Hydra-Token"] = token
  tyk.log("ResponseHook END", logLevel)
  return response
