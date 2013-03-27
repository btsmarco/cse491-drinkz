import drinkz.Napp, urllib
import drinkz.db
from drinkz import recipes

def test_input():
    drinkz.db._reset_db()
    drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    drinkz.db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    drinkz.db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    drinkz.db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    drinkz.db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    drinkz.db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    drinkz.db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch','2 oz')])
    r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),\
                                                ('vermouth', '1.5 oz')])
    drinkz.db.add_recipe(r)
    drinkz.db.add_recipe(r2)

def test_index():
    #making an empty environ dictionary
    environ = {}
    environ['PATH_INFO'] = '/'
   
    #making a start_response function 
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = drinkz.Napp.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Visit:') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_form_recv():
    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO',
                                                    lastname='BAR'))
    environ['PATH_INFO'] = '/recv'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = drinkz.Napp.SimpleApp()
    results = app_obj(environ, my_start_response)
    
    text = "".join(results)
    status = d['status']
    headers = d['headers']

    assert text.find("Amount:") != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
