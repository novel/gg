#!/usr/bin/env python

import md5
import os
import os.path
import sys
import time
import urllib

# define exceptions
class Error403(Exception): pass
class GoGridException(Exception): pass

class GoGridClient:
  """gogrid api client"""
  default_params = {'format':'csv', 'v':'1.0'}
  server = 'https://api.gogrid.com/api'
  api_key = None
  secret = None
  
  def __init__(self, key='', secret='', server=None):
    if key != "":
        self.api_key = key
    if secret != "":
        self.secret = secret
    if server is not None:
        self.server = server

    # if the options weren't given via constructor, try
    # to read them from file
    if self.api_key is None or self.secret is None:
        lines = open(os.path.expanduser("~/.ggrc"), 'r').readlines()
        self.api_key, self.secret = lines[0].split(":")

    gg_server = os.getenv('GG_SERVER')
    if gg_server is not None:
        self.server = gg_server

    self.default_params['api_key'] = self.api_key.strip()
    self.default_params['secret'] = self.secret.strip()
  
  def getRequestURL(self, method, params={}):
    """ constructs a call url from a given method with params """
    requestURL = self.server + '/' + method + '?'
    call_params = self.default_params.copy()
    call_params.update(params)
    call_params['sig'] = self.getSignature(call_params['api_key'],call_params['secret'])
    del call_params['secret']
    requestURL += urllib.urlencode(call_params)
    return requestURL
  
  def getSignature(self, key, secret):
    """ create sig from md5 of key + secret + time """
    m = md5.new(key + secret + str(int(time.time())))

    return m.hexdigest()
        
  def sendAPIRequest(self, method, params={}):
    """ send a request and return response """
    url = self.getRequestURL(method, params)
    try:
        f = urllib.urlopen(url)
    except IOError, err:
        print "%s: %s" % (self.server, err.strerror[1])
        sys.exit(1)

    result = f.read()

    if "403 Not Authorized" in result:
        raise Error403, "Authorization error, check credentials and your time settings."

    if "FAILURE" in result:
        raise GoGridException(result.splitlines()[2].replace(",", ": "))

    return result

if __name__ == "__main__":
    client = GoGridClient()

    # ma   ke some calls
    print client.sendAPIRequest("grid/server/list")
