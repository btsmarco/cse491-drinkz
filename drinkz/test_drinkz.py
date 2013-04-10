"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data, recipes

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '2000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '10 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 3295.735, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000.54 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.54, amount

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_bottle_types_2():
    db._reset_db()

    data = "J,B"
    fp = StringIO(data)            # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0

def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_bottle_types_2():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-2.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_1():
    #tests for the comments
    scriptpath = 'bin/load-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/inventory-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_2():
    #tests for empty lines at the end of files 
    scriptpath = 'bin/load-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/inventory-data-2.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x

def test_show_liquor_amounts():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    db.show_liquor_amounts()

def test_check_available_recipes():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '5 oz')

    #r should be all set
    r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])

    
    db.add_recipe(r)
    r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                            ('vermouth', '1.5 oz')])

    db.add_recipe(r2)

    avR = db.check_available_recipes()

    assert len(avR) == 1, avR
    assert avR[0] == r, avR[0]

def test_check_available_recipes_2():
    db._reset_db()


    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '7 oz')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '4 oz')

    
    r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])

    r2 = recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth','1.5 oz')])

    r3 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                            ('vermouth', '1.5 oz')])


    db.add_recipe(r)
    db.add_recipe(r2)
    db.add_recipe(r3)

    avR = db.check_available_recipes()

    assert len(avR) == 1, avR
    assert avR[0] == r3, avR[0].name

def test_bulk_load_recipes():
    db._reset_db()

    data = "whiskey bath, blended scotch, 6 liter"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_recipes(fp)

    assert db.get_recipe('whiskey bath')
    assert n == 1, n

def test_bulk_load_recipes_2():
    db._reset_db()

    data = """ 4 oz\n#  whiskey bath, blended scotch, 6 liter\n\nvomit inducing martini, 6 oz, vermouth, 1.5 oz
    """ 

    fp = StringIO(data)            # make this look like a file handle
    n = load_bulk_data.load_recipes(fp)

    assert n == 0,n


