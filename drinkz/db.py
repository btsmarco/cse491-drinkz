"""
Database functionality for drinkz information.
I have choosen to store recipes in dictionaries, because it is very
easy to get the ingredients of a recipe simply by using its name as 
a key and the recipe as a value. 
"""
import math, sqlite3, os, cPickle, shutil
from recipes import Recipe
from parties import Party 
from cPickle import dump, load

if __name__ == '__main__':
    os.chdir(r'/user/botrosma/cse491/cse491-drinkz/drinkz')

db = sqlite3.connect('inv.db')
c = db.cursor()

pdb = sqlite3.connect('parties.db')
p = pdb.cursor()

#c.execute('CREATE TABLE bottle_types (mnf TEXT, lqr TEXT, typ TEXT)')
#c.execute('CREATE TABLE inventory (mnf TEXT, lqr TEXT, amnt FLOAT)')
#c.execute('CREATE TABLE recipes (name TEXT, cmpts TEXT)')

#p.execute('CREATE TABLE parties (HName TEXT,HNum TEXT, loc TEXT, date TEXT,crash INTEGER, inv TEXT, music TEXT, restu TEXT)')

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    c.execute('DELETE FROM bottle_types')
    c.execute('DELETE FROM inventory')
    c.execute('DELETE FROM recipes')

    p.execute('DELETE FROM parties')

def prepare_parties():
    p = parties.Party('251 river st, East Lansing MI, 48823','Josh Mac','5173338888','4 April 2013',5,[('radioactive','imagine dragons'),('titanium','guetta'),('gaungam style','Psy')],[('Johhny walker','black label','blended scotch'),('Rossi','extra dry vermouth','vermouth')],['taco bell','McDonels'])

    p2 = parties.Party('288 bailey st, East Lansing MI, 48823','Amy Scott','5173562978','15 April 2013',2,[('Just give me a reason' ,'Pink Ruess'),('Carry On','Fun'),('Gentlemen','Psy')],[('Johhny walker','black label','blended scotch'),('Gray Goose','vodka','unflavored vodka')],['taco bell','picking express'])
    add_party(p)
    add_party(p2)

#Not sure if they are of any use now
def save_db(filename):
    if __name__ == '__main__':
        os.chdir(r'/user/botrosma/cse491/cse491-drinkz/drinkz')
#    f1 = filename +'_inv.db'
#    f2 = filename +'_parties.db'
#    shutil.copy('inv.db',f1)
#    shutil.copy('parties.db',f2)
#    fp = open(filename, 'wb')

#    tosave = (_bottle_types_db, _inventory_db, _recipes_db)
#    dump(tosave, fp)

#    fp.close()

def load_db(filename):
    try:
        os.unlink('inv.db')
    except OSError:
        pass
    try:
        os.unlink('parties.db')
    except OSError:
        pass

#    f1 = filename +'_inv.db'
#    f2 = filename +'_parties.db'

 #   os.unlink(f1)
 #   os.unlink(f2)
 #   shutil.copy(f1,'inv.db')
 #   shutil.copy(f2,'parties.db')

    db = sqlite3.connect('inv.db')
    c = db.cursor()

    pdb = sqlite3.connect('parties.db')
    p = pdb.cursor()

#    global _bottle_types_db, _inventory_db, _recipes_db
#    fp = open(filename, 'rb')

#    loaded = load(fp)
#    (_bottle_types_db, _inventory_db, _recipes_db) = loaded

 #   fp.close()

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
    c.execute('INSERT INTO bottle_types (mnf,lqr,typ) VALUES (?,?,?)',(mfg, liquor, typ))
    db.commit()

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

def get_bottle_types():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    c.execute('SELECT * FROM bottle_types')
    bottle_types_db = c.fetchall()
    for (m, l,t) in bottle_types_db:
        yield m, l,t


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

def add_party(party):
    """adding the party into the database of paries with"""
    lqr = cPickle.dumps(party.lqr_cab)
    music = cPickle.dumps(party.music)
    restu = cPickle.dumps(party.restu)
    p.execute('INSERT INTO parties (HName,HNum,loc,date,crash,inv,music,restu)VALUES(?,?,?,?,?,?,?,?)',(party.H_name,party.H_num,party.loc,party.date,party.crash,lqr,music,restu))
    db.commit()

def get_party(HName):
    """returns a party"""
    p.execute('SELECT * FROM parties')
    parties_db = p.fetchall()
    
    for par in parties_db:
        if HName == par[0]:
            return Party(par[2],par[0],par[1],par[3],par[4],cPickle.loads(str(par[5])),cPickle.loads(str(par[6])),cPickle.loads(str(par[7])))
    return 0

def get_all_parties_list():
    """returns all  parties"""
    p.execute('SELECT * FROM parties')
    parties_db = p.fetchall()
    
    for par in parties_db:
        yield list(par[0],par[1],par[2],par[3],par[4],cPickle.loads(str(par[5])),cPickle.loads(str(par[6])),cPickle.loads(str(par[7])))

def get_all_parties():
    """ returns the whole dictionary of recipes or a list of recipes"""
    p.execute('SELECT * FROM parties')
    parties_db = p.fetchall()

    for par in parties_db:
        party = get_party(par[0]) 
        yield party


