import app, urllib
import db
from drinkz import recipes

def test_index():
    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/'
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Hi this Project 4 for CSE 491, hopefully you enjoy it :D') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_recipes():
    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/recipes'
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_inventory():
    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/inventory'
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Johnnie Walker') != -1, text
    assert text.find('extra dry vermouth') != -1, text
    assert text.find("Uncle Herman's") != -1, text
    assert text.find('1000 ml') != -1, text

    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_liquor_types():
    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/liquor_types'
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Johnnie Walker, black label, blended scotch') != -1, text
    assert text.find("Uncle Herman's, moonshine, blended scotch") != -1, text
    assert text.find('Gray Goose, vodka, unflavored vodka') != -1, text
    assert text.find('Rossi, extra dry vermouth, vermouth') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_forum():
    #making an empty environ dictionary
    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(amount='1',unit='oz'))

    environ['PATH_INFO'] = '/recv_ml'

   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    assert text.find('Amount: 29.573 ml. ') != -1, text

    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

