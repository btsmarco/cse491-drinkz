import Napp, urllib, db, simplejson 
from cStringIO import StringIO
from drinkz import recipes


def test_rpc_convert():
    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['CONTENT_LENGTH'] = '1' 
    d = dict(method= 'convert_to_ml',params=['1 oz'], id=1)
   # d = "method:'convert_to_ml',params:['1 oz'], id:1"
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded) 
    environ['REQUEST_METHOD'] = 'convert_to_mlPOST' 
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = Napp.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('ml') != -1, text
    assert ('Content-Rype', 'application/json') in headers
    assert status == '200 OK'



"""
def test_forum():
    #making an empty environ dictionary
    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(amount='1',unit='oz'))

    environ['PATH_INFO'] = '/recv'

   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = Napp.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    assert text.find('Amount: 29.573 ml. ') != -1, text

    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
"""
