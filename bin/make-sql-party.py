import sqlite3, os

try:
    os.unlink('../drinkz/parties.db')
except OSError:
    pass

os.chdir(r'/user/botrosma/cse491/cse491-drinkz/drinkz')
pdb = sqlite3.connect('../drinkz/parties.db')
p = db.cursor()

p.execute('CREATE TABLE parties (HName TEXT,HNum TEXT, loc TEXT, date TEXT,crash INTEGER, inv TEXT, music TEXT, restu TEXT)')
db.commit()
