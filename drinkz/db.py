"""
Database functionality for drinkz information.
"""
import math
# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set([])
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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
            if("ml") in amount:
                amount = amount.strip('ml')
                amount = amount.strip()
                amounts += int(amount)
            elif("oz") in amount:
                amount = amount.strip('oz')
                amount = amount.strip()
                amounts += math.floor(int(amount)*29.57)#1 oz=29.57ml
            _inventory_db[(mfg, liquor)] = amounts 
        else:
            amounts = 0
            if("ml") in amount:
                amount = amount.strip('ml')
                amount = amount.strip()
                amounts += int(amount)
            elif("oz") in amount:
                amount = amount.strip('oz')
                amount = amount.strip()
                amounts += math.floor(int(amount)*29.57)#1 oz=29.57ml
            _inventory_db[(mfg, liquor)] = amounts 

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
