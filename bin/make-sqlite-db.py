import sqlite3, os

try:
    os.unlink('../drinkz/inv.db')
except OSError:
    pass

os.chdir(r'/user/botrosma/cse491/cse491-drinkz/drinkz')
db = sqlite3.connect('../drinkz/inv.db')
c = db.cursor()

pdb = sqlite3.connect('../drinkz/parties.db')
p = pdb.cursor()


#Create the table
c.execute('CREATE TABLE bottle_types (mnf TEXT, lqr TEXT, typ TEXT)')
c.execute('CREATE TABLE inventory (mnf TEXT, lqr TEXT, amnt FLOAT)')
c.execute('CREATE TABLE recipes (name TEXT, cmpts TEXT)')

p.execute('CREATE TABLE parties (HName TEXT,HNum TEXT, loc TEXT, date TEXT,crash INTEGER, inv TEXT, music TEXT, restu TEXT)')

