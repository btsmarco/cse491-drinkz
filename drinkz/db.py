"""
Database functionality for drinkz information.
I have choosen to store recipes in dictionaries, because it is very
easy to get the ingredients of a recipe simply by using its name as 
a key and the recipe as a value. 
"""
import math, sqlite3, os, cPickle
from recipes import Recipe
from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
_recipes_db = {}

try:
    os.unlink('../drinkz/inv.db')
except OSError:
    pass

db = sqlite3.connect('inv.db')
c = db.cursor()

#c.execute('CREATE TABLE bottle_types (mnf TEXT, lqr TEXT, typ TEXT)')
#c.execute('CREATE TABLE inventory (mnf TEXT, lqr TEXT, amnt FLOAT)')
#c.execute('CREATE TABLE recipes (name TEXT, cmpts TEXT)')
db.commit()


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    c.execute('DELETE FROM bottle_types')
    c.execute('DELETE FROM inventory')
    c.execute('DELETE FROM recipes')

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
    c.execute('INSERT INTO bottle_types (mnf,lqr,typ) VALUES (?,?,?)',(mfg, liquor, typ))
    db.commit

def _check_bottle_type_exists(mfg, liquor):
    c.execute('SELECT * FROM bottle_types')
    bottle_types_db = c.fetchall()
    for (m, l, _) in bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."

    c.execute('SELECT * FROM inventory')
    inventory_db = c.fetchall()

    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    else:
        bulb = False
        for i in inventory_db:
            if mfg in i[0]:
                if liquor in i[1]:
                    bulb = True
        if bulb:
            c.execute('SELECT amnt FROM inventory WHERE mnf=? AND lqr=?',(mfg,liquor))
            ext_amnt = c.fetchall()[0][0]
            num = convert_to_ml(amount)

            c.execute('UPDATE inventory SET amnt = ? WHERE mnf =? AND lqr=?',(ext_amnt+num,mfg,liquor))
        else:
            num = convert_to_ml(amount)

            c.execute('INSERT INTO inventory (mnf,lqr,amnt) VALUES(?,?,?)',(mfg, liquor, num))
    db.commit()

    # just add it to the inventory database as a tuple, for now.
    #_inventory_db.append((mfg, liquor, amount))

def check_inventory(mfg, liquor):
    c.execute('SELECT * FROM inventory')
    inventory_db = c.fetchall()

    for (m, l, _) in inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    c.execute('SELECT amnt FROM inventory WHERE mnf=? AND lqr=?',(mfg,liquor))
    amnt = c.fetchall()[0][0]

    return amnt

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    c.execute('SELECT * FROM inventory')
    inventory_db = c.fetchall()
    for (m, l,_) in inventory_db:
        yield m, l

def show_liquor_amounts():
    "Print all the liquor types and amounts in the inventory. "
    c.execute('SELECT * FROM bottle_types')
    bottle_types_db = c.fetchall()

    print 'Manufacturer\tLiquor\t\tAmount'
    print '------------\t------\t\t------'
    for (mfg, liquor, _) in bottle_types_db:
        print "%s\t%s\t%d"%(mfg, liquor, get_liquor_amount(mfg, liquor))

def add_recipe(r):
    """adding the recipe into the dictionary of recipes with
    name as key and the recipe as a value"""
    c.execute('SELECT * FROM recipes')
    recipes_db = c.fetchall()

    bulb = True;
    for rec in recipes_db:
        if r.name in rec[0]:
            bulb = False;

    if bulb:
        pck = cPickle.dumps(r.comp)
        c.execute('INSERT INTO recipes (name,cmpts) VALUES(?,?)',(r.name,pck))
    else:
        err = "Sorry the name %s is already used, please use a different name."%r.name
        raise DuplicateRecipeName(err)

def get_recipe(name):
    """returns a recipe"""
    c.execute('SELECT * FROM recipes')
    recipes_db = c.fetchall()

    for rec in recipes_db:
        if name in rec[0]:
            return Recipe(name,cPickle.loads(str(rec[1])))
    return 0

def get_all_recipes():
    """ returns the whole dictionary of recipes or a list of recipes"""
    c.execute('SELECT * FROM recipes')
    recipes_db = c.fetchall()

    for rec in recipes_db:
        r = Recipe(rec[0],cPickle.loads(str(rec[1])))
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

def check_inventory_for_type(typ):
    c.execute('SELECT * FROM bottle_types')
    bottle_types_db = c.fetchall()

    max_amount = 0
    for (M,L,T) in bottle_types_db:
        if (T == typ):
            I_amount = get_liquor_amount(M,L)
            if (max_amount < I_amount):
                max_amount = I_amount

    return max_amount 

def check_available_recipes():
    """ The function needs to return a list of recipes that could be made with
    the inventory available. The function uses recipe.need_ingrediants(), if
    nothing is returned we add it to the list"""
    c.execute('SELECT * FROM recipes')
    recipes_db = c.fetchall()

    av = []
    for rec in recipes_db:
        r = Recipe(rec[0],cPickle.loads(str(rec[1])))
        if (r.need_ingredients() == []):
            av.append(r)
    
    return av 

