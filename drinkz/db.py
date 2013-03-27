"""
Database functionality for drinkz information.
I have choosen to store recipes in dictionaries, because it is very
easy to get the ingredients of a recipe simply by using its name as 
a key and the recipe as a value. 
"""
import math
from recipes import Recipe

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
_recipes_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db , _recipes_db
    _bottle_types_db = set([])
    _inventory_db = {}
    _recipes_db = {}

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

class CorruptLine(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    else:
        if (mfg, liquor) in _inventory_db:
            amounts = _inventory_db[(mfg, liquor)] 
            num = convert_to_ml(amount)

            _inventory_db[(mfg, liquor)] = amounts + num 
        else:
            num = convert_to_ml(amount)

            _inventory_db[(mfg, liquor)] = num

    # just add it to the inventory database as a tuple, for now.
    #_inventory_db.append((mfg, liquor, amount))

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."

    amounts = _inventory_db[(mfg, liquor)] 

    return amounts

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l

def show_liquor_amounts():
    "Print all the liquor types and amounts in the inventory. "
    print 'Manufacturer\tLiquor\t\tAmount'
    print '------------\t------\t\t------'
    for (mfg, liquor, _) in _bottle_types_db:
        print "%s\t%s\t%d"%(mfg, liquor, get_liquor_amount(mfg, liquor))

def add_recipe(r):
    """adding the recipe into the dictionary of recipes with
    name as key and the recipe as a value"""
    if (r.name not in _recipes_db.keys()):
        _recipes_db[r.name] = r
    else:
        err = "Sorry the name %s is already used, please use a different name."%r.name
        raise DuplicateRecipeName(err)

def get_recipe(name):
    """returns a recipe"""
    if(name in _recipes_db.keys()):
        return _recipes_db[name]
    else:
        return 0

def get_all_recipes():
    """ returns the whole dictionary of recipes or a list of recipes"""
    for n, r in _recipes_db.iteritems():
        yield r

def convert_to_ml(amount):
    if("ml") in amount:
        amount = amount.strip('ml')
        amount = amount.strip()
        result = float(amount)
    elif("oz") in amount:
        amount = amount.strip('oz')
        amount = amount.strip()
        result = (float(amount)*29.5735)#1 oz=29.57ml
    elif("gallon") in amount:
        amount = amount.strip('gallon')
        amount = amount.strip()
        result = (float(amount)*3785.41)
    elif("liter") in amount:
        amount = amount.strip('liter')
        amount = amount.strip()
        result = (float(amount)*1000)
    else:
        assert 0, amount

    return result 


#    return 0

def check_inventory_for_type(typ):
    max_amount = 0
    for (M,L,T) in _bottle_types_db:
        if (T == typ):
            I_amount = get_liquor_amount(M,L)
            if (max_amount < I_amount):
                max_amount = I_amount

    return max_amount 


