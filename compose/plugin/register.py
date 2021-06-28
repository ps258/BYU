from tyk.decorators import *
from gateway import TykGateway as tyk

import os
import sys
bundle_dir = os.path.abspath(os.path.dirname(__file__))
for lib_dir in [ 'vendor/lib/python3.7/site-packages/' ]:
  vendor_dir = os.path.join(bundle_dir, lib_dir)
  sys.path.append(vendor_dir)

import jwt
import json
import requests
import datetime

# Load the certificate. Stored in the bundle but could be a string in this file too
cert_file = "jwt-signing-key.pem"
cert_file = os.path.join(bundle_dir, cert_file)
private_key = open(cert_file).read()

@Hook
def ResponseHook(request, response, session, metadata, spec):
  logLevel = "info"
  tyk.log("ResponseHook START", logLevel)
  # decode the response from upstream. Should contain the auth token we key on
  # the time that the JWT lives in redis
  token = response.raw_body.decode()
  # load the config data from the API definition
  api_config_data = json.loads(spec['config_data'])
  # show all the data structures
  #tyk.log("ResponseHook request object: " + str(vars(request)), logLevel)
  #tyk.log("ResponseHook response object: " + str(response), logLevel)
  #tyk.log("ResponseHook session object: " + str(session), logLevel)
  #tyk.log("ResponseHook metadata object: " + str(metadata), logLevel)
  #tyk.log("ResponseHook spec object: " + str(spec), logLevel)
  #tyk.log("ResponseHook: upstream returned {0}".format(response.status_code), logLevel)
  # show the config_data fields
  #tyk.log("config_data is: " + spec['config_data'], logLevel)
  #tyk.log("analytics is: " + api_config_data['analytics'], logLevel)
  #tyk.log("introspect URL is: " + introspect_URL, logLevel)
  introspect_URL = api_config_data['introspect']
  analytics_field = api_config_data['analytics']
  tokenLife = api_config_data['token_life']
  introspect_params = {'token': token }
  # connect to the introspection URL and introspect the token
  introspection = requests.get(introspect_URL, params=introspect_params)
  introspect_data = json.loads(introspection.text)
  # log the details for debugging
  #tyk.log("Introspection: " + introspection.text, logLevel)
  #tyk.log("analytics_field: " + analytics_field, logLevel)
  #tyk.log("analytics_value: " + introspect_data[analytics_field], logLevel)
  # build the jwt
  j = jwt.encode({'scope': 'universal', 'sub': 'Subject', analytics_field: introspect_data[analytics_field], 'token': token, 'exp': introspect_data['exp'], "iat": datetime.datetime.utcnow()}, private_key, algorithm='RS256')
  # save to redis
  tyk.store_data(token, j, tokenLife)
  tyk.log("JWT: " + j, logLevel)
  # stick the token into the headers for good measure
  response.headers["Hydra-Token"] = token
  tyk.log("ResponseHook END", logLevel)
  return response
