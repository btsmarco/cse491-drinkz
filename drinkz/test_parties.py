"""
Tests basic party API.
"""

import unittest
from . import db, parties 

class TestBasicRecipeStuff(unittest.TestCase):
    def setUp(self):                    # This is run once per test, before.
        db._reset_db()

    def tearDown(self):                 # This is run once per test, after.
        pass

    def test_add_party_1(self):
        x = list(db.get_all_parties())
        assert not x                    # should be no partys
        
        p = parties.Party('251 river st, East Lansing MI, 48823','Josh Mac','5173338888','4 April 2013',5,[('radioactive','imagine dragons'),('titanium','guetta'),('gaungam style','Psy')],[('Johhny walker','black label','blended scotch'),('Rossi','extra dry vermouth','vermouth')],['taco bell','McDonels'])

        db.add_party(p)

        x = list(db.get_all_parties())
        assert len(x) == 1              # should be only one party
        assert p in x

    def test_get_party_1(self):
        p = parties.Party('288 bailey st, East Lansing MI, 48823','Amy Scott','5173562978','15 April 2013',2,[('Just give me a reason' ,'Pink Ruess'),('Carry On','Fun'),('Gentlemen','Psy')],[('Johhny walker','black label','blended scotch'),('Gray Goose','vodka','unflavored vodka')],['taco bell','picking express'])

        db.add_party(p)

        x = db.get_party('Amy Scott')
        assert x == p, x.H_name

    def test_get_party_2(self):
        x = db.get_party('Marc James')
        assert not x, x                    # no such party

