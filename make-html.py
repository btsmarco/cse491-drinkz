#! /usr/bin/env python
import os
import drinkz.db
from drinkz import recipes

try:
    os.mkdir('html') 
except OSError:
    # already exists
    pass
#
#########################################
#

#this resets all the lists and makes loads the database
drinkz.db._reset_db()
drinkz.db.load_db('Database')

#drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
#drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

#drinkz.db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
#drinkz.db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

#drinkz.db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
#drinkz.db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

#drinkz.db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
#drinkz.db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

#r = recipes.Recipe('scotch on the rocks', [('blended scotch','2 oz')])
#r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
#                                            ('vermouth', '1.5 oz')])
#drinkz.db.add_recipe(r)
#drinkz.db.add_recipe(r2)
#
#########################################
#
fp = open('html/index.html', 'w')
print >>fp,"""
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
		<title>Drinkz</title>
		<link rel="stylesheet" href="../css/main.css" type="text/css" media="screen">
		<script type="text/javascript" src="js/app.js"></script>
	</head>
	<body>
		<div class="container">
			<p class="head">Drinkz</p>
			<nav>
				<div class="navbox">
					<a href="index.html">home</a>
				</div>
				<div class="navbox">
					<a href="recipes.html">Recipes</a>
				</div>
				<div class="navbox">
					<a href="inventory.html">Inventory</a>
				</div>
				<div class="navbox">
					<a href="liquor_types.html">Liquor types</a>
				</div>
			</nav>

			<article>
			<p>Hi this Project 3 for CSE 491, hopefully you enjoy it :D</p>
			</article>

		</div>
		<img id="bottom" src="../img/signituretrans.png" alt="signiture"/>
	</body>
</html>
"""

fp.close()

#
#########################################
#

fp = open('html/recipes.html', 'w')
print >>fp,"""
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
		<title>Drinkz</title>
		<link rel="stylesheet" href="../css/main.css" type="text/css" media="screen">
		<script type="text/javascript" src="js/app.js"></script>
	</head>
	<body>
		<div class="container">
			<p class="head">recipes</p>
			<nav>
				<div class="navbox">
					<a href="index.html">home</a>
				</div>
				<div class="navbox">
					<a href="recipes.html">Recipes</a>
				</div>
				<div class="navbox">
					<a href="inventory.html">Inventory</a>
				</div>
				<div class="navbox">
					<a href="liquor_types.html">Liquor types</a>
				</div>
			</nav>
"""

print >>fp,"""<table border='1' margin='50px'>
<tr>
<td><strong>Recipes</strong></td>
<td><strong>Available?</strong></td>
</tr>
"""
for k,v in drinkz.db._recipes_db.iteritems():
    print >>fp, "<tr><td>"
    print >>fp, k
    print >>fp, "</td><td>"
    if (v.need_ingredients):
        print >>fp, "no"
    else:
        print >>fp, "ya"
    print >>fp, "</td></tr>"
print >>fp,"</table>"

print >>fp,"""

		</div>
		<img id="bottom" src="../img/signituretrans.png" alt="signiture"/>
	</body>
</html>
"""

fp.close()

#
#########################################
#
fp = open('html/inventory.html', 'w')
print >>fp,"""
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
		<title>Drinkz</title>
		<link rel="stylesheet" href="../css/main.css" type="text/css" media="screen">
		<script type="text/javascript" src="js/app.js"></script>
	</head>
	<body>
		<div class="container">
			<p class="head">inventory</p>
			<nav>
				<div class="navbox">
					<a href="index.html">home</a>
				</div>
				<div class="navbox">
					<a href="recipes.html">Recipes</a>
				</div>
				<div class="navbox">
					<a href="inventory.html">Inventory</a>
				</div>
				<div class="navbox">
					<a href="liquor_types.html">Liquor types</a>
				</div>
			</nav>
"""

print >>fp,"""<table border='1' margin='50px'>
<tr>
<td><strong>Manufacturer</strong></td>
<td><strong>Liquor</strong></td>
<td><strong>Amount</strong></td>
</tr>
"""

for k,v in drinkz.db._inventory_db.iteritems():
    print >>fp, "<tr><td>"
    print >>fp, k[0]
    print >>fp, "</td><td>"
    print >>fp, k[1]
    print >>fp, "</td><td>"
    print >>fp, v, " ml"
    print >>fp, "</td></tr>"
print >>fp,"</table>"

print >>fp,"""
		</div>
		<img id="bottom" src="../img/signituretrans.png" alt="signiture"/>
	</body>
</html>
"""

fp.close()
#########################################

fp = open('html/liquor_types.html', 'w')
print >>fp,"""
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
		<title>Drinkz</title>
		<link rel="stylesheet" href="../css/main.css" type="text/css" media="screen">
		<script type="text/javascript" src="js/app.js"></script>
	</head>
	<body>
		<div class="container">
			<p class="head">liquor</p>
			<nav>
				<div class="navbox">
					<a href="index.html">home</a>
				</div>
				<div class="navbox">
					<a href="recipes.html">Recipes</a>
				</div>
				<div class="navbox">
					<a href="inventory.html">Inventory</a>
				</div>
				<div class="navbox">
					<a href="liquor_types.html">Liquor types</a>
				</div>
			</nav>
            <h2>All the liquor types available: </h2>
"""

print >>fp,"<ul>"
for (mfg, lqr,typ) in drinkz.db._bottle_types_db:
    print >>fp, "<li>"
    print >>fp, mfg," , ",lqr, " , ",typ
print >>fp,"</ul>"
print >>fp,"""
		</div>
		<img id="bottom" src="../img/signituretrans.png" alt="signiture"/>
	</body>
</html>
"""
fp.close()

