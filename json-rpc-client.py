#! /usr/bin/env python
import sys
import simplejson
import urllib2

def call_remote(base, method, params, id):
    # determine the URL to call
    url = base + 'rpc'

    # encode things in a dict that is then converted into JSON
    d = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(d)

    # specify appropriate content-type
    headers = { 'Content-Type' : 'application/json' }

    # call remote server
    req = urllib2.Request(url, encoded, headers)

    # get response
    response_stream = urllib2.urlopen(req)
    json_response = response_stream.read()

    # decode response
    response = simplejson.loads(json_response)

    # return result
    return response['result']

if __name__ == '__main__':
    #sys.argv[1] is the url since it is the second argument on the command line
    server_base = sys.argv[1]

    print 'Convert to ml!', call_remote(server_base,method='convert_units_to_ml', params=['1 oz' ], id=1)
    
    print 'recipes_names:', call_remote(server_base, method='recipes_names', params=[], id=1)
    print 'liquor_inventory:', call_remote(server_base, method='liquor_inventory', params=[], id=1)
