#!/usr/bin/env python

import md5
import time
import urllib
import os.path
import sys

# define exceptions
class Error403(Exception): pass

class GoGridClient:
  """gogrid api client"""
  default_params = {'format':'csv', 'v':'1.0'}
  server = 'https://api.gogrid.com/api'
  api_key = None
  secret = None
  
  def __init__(self, key='', secret=''):
    if key != "":
        self.api_key = key
    if secret != "":
        self.secret = secret
    
    # if the options weren't given via constructor, try
    # to read them from file
    if self.api_key is None or self.secret is None:
        fd = open(os.path.expanduser("~/.ggrc"), 'r')
        self.api_key, self.secret = fd.readlines()[0].split(":")

    self.default_params['api_key'] = self.api_key.strip()
    self.default_params['secret'] = self.secret.strip()
  
  def getRequestURL(self,method,params={}):
    """ constructs a call url from a given method with params """
    requestURL = self.server+'/'+method+'?'
    call_params = self.default_params.copy()
    call_params.update(params)
    call_params['sig'] = self.getSignature(call_params['api_key'],call_params['secret'])
    del call_params['secret']
    requestURL += urllib.urlencode(call_params)
    return requestURL
  
  def getSignature(self,key,secret):
    """ create sig from md5 of key + secret + time """
    m = md5.new(key+secret+str(int(time.time())))

    return m.hexdigest()
        
  def sendAPIRequest(self,method,params={}):
    """ send a request and return response """
    url = self.getRequestURL(method,params)
    f = urllib.urlopen(url)
    result = f.read()

    if "403 Not Authorized" in result:
        raise Error403, "Authorization error, check credentials and your time settings."

    if "FAILURE" in result:
        print result.splitlines()[2].replace(",", ": ")
        sys.exit(1)

    return result

if __name__ == "__main__":
    client = GoGridClient()

    # ma   ke some calls
    print client.sendAPIRequest("grid/server/list")
