import db
class Recipe():
    def __init__(self,name,components):
        """ This is the constructor for the class recipe,
        It takes in two variables, a string name and a list of
        2-tuples that represent the components
        It saves the info in 3 variables, a self.name as a string,
        a self.comp as the exact list and a dictionary of components
        with the name as key and value is amount needed"""
        if(name):
            self.name = name
        if(components):
            self.comp = components
            self.D_comp = {}
            for tup in self.comp:
                self.D_comp[tup[0]] = tup[1]

    def need_ingredients(self):
        """ This methode takes in the recipe and returns how many
        components are needed to complete the recipe.  It returns
        the components in the form of a list of 2-tuples"""
        needed = []
        
        for t, amount in self.comp:
            in_inventory = db.check_inventory_for_type(t)
            required = db.convert_to_ml(amount)

            if in_inventory < required:
                print required
                print in_inventory
                needed.append((t,required - in_inventory))
            else:
                continue

        return needed

    def __eq__(self,a):
        if self.name == a.name and self.comp == a.comp:
            return 1
        else:
            return 0
