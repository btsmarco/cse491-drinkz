import app, urllib, urllib2, db, simplejson 
from cStringIO import StringIO
from drinkz import recipes

def test_rpc_convert():
    #making an empty environ dictionary
    db.load_db('Database')
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    d = dict(method= 'convert_units_to_ml',params=['1 oz'], id=1)
    dataE = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(dataE) 
    environ['CONTENT_LENGTH'] = len(dataE) 
    environ['REQUEST_METHOD'] = 'POST' 
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
   
    assert '29.5735' in results[0], results[0]
    assert text.find('29.5735') != -1, text
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'

def test_rpc_recipes():
    db.load_db("Database")

    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    d = dict(method= 'recipes_names',params=[], id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded) 
    environ['CONTENT_LENGTH'] = len(encoded) 
    environ['REQUEST_METHOD'] = 'POST' 
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
  
    assert text.find('scotch on the rocks') != -1, text
    assert text.find('vodka martini') != -1, text
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'

def test_rpc_inventory():
    db.load_db('Database')

    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    d = dict(method= 'liquor_inventory',params=[], id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded) 
    environ['CONTENT_LENGTH'] = len(encoded) 
    environ['REQUEST_METHOD'] = 'POST' 
   
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
    assert text.find('Rossi') != -1, text
    assert text.find('moonshine') != -1, text
    assert text.find('vodka') != -1, text
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'

def test_rpc_add_liquor_type():
    db.load_db('Database')

    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    d = dict(method= 'add_liquor_type',params=[("Marco Botros","vodka","like the moon")], id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded) 
    environ['CONTENT_LENGTH'] = len(encoded) 
    environ['REQUEST_METHOD'] = 'POST' 
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
   
    assert db._check_bottle_type_exists('Marco Botros', 'vodka')
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'

def test_rpc_add_to_inventory():
    db._reset_db()
    db.add_bottle_type("Marco Botros","vodka","like the moon")
    #db.load_db('Database')

    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    d = dict(method= 'add_to_inventory',params=[("Marco Botros","vodka","3 oz")], id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded) 
    environ['CONTENT_LENGTH'] = len(encoded) 
    environ['REQUEST_METHOD'] = 'POST' 
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
  	
    assert db.check_inventory('Marco Botros', 'vodka'),db._inventory_db
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'

def test_rpc_add_to_inventory():
    db.load_db('Database')

    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    d = dict(method= 'add_recipe',params=['THE DUDE',[("Marco Botros","3 oz"),('vodka','1 liter')]], id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO(encoded) 
    environ['CONTENT_LENGTH'] = len(encoded) 
    environ['REQUEST_METHOD'] = 'POST' 
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
  	
    assert db.get_recipe('THE DUDE'),db._recipes_db
    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
