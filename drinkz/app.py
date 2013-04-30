from wsgiref.simple_server import make_server
import urlparse, simplejson, db, recipes, os
from jinja2 import Environment  

dispatch = {
    '/' : 'index',
    '/recipes' : 'recipes',
    '/ajaxform' : 'ajaxform',
    '/error' : 'error',
    '/inventory' : 'inventory',
    '/liquor_types' : 'liquor_types',
    '/form' : 'form',
    '/recv_ml' : 'recv_ml',
    '/recv_li' : 'recv_li',
    '/recv_in' : 'recv_in',
    '/recv_re' : 'recv_re',
    '/recv_re_2' : 'recv_re_2',
    '/rpc'  : 'dispatch_rpc',
    '/ml'  : '1',
    '/lt'  : '2',
    '/in'  : '3',
    '/re'  : '4'
}

html_headers = [('Content-type', 'text/html')]

db.load_db("Database")

begining = """ \
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
        <title> %s </title>
        <script>
            function alertThem(){
                alert("Hi you are awesome");
            }
        </script>
        <style type="text/css"> 
            h2{
                color: #B0171F;
            }
            html, body{
                height:100%%;
            }
            .wrapper{
                width:auto;
            }
            .container{
                background:white;
                min-height:100%%;
                padding:30px 50px 50px 30px ;
                width:550px;
            	margin-left:auto;
                margin-right:auto;
                border:5px solid;
                border-color:#ECC201;
            }
            .container2{
                border-color:#0E78A0 !important;
            }
            .link{
                font-family: 'Open sans', sans-serif;
                text-align:center;
                font-size: 30px;
            }
            a:link{
                text-decoration:none;
                color:#63B8FF;
            }
            article{
                font-family: 'Beunard', serif;
                font-size: 20px;
            }
            .note{
                font-family: 'Beunard', serif;
                font-size: 20px;
                color:#B0171F;
            }
            .icon{
                width:130px;
                height:auto;
                position:absolute;
                margin-top:150px;
                margin-left:80px;
                border:1px solid;
            }
            .icon:hover{
                background:white;
            }
            #bottom{
                width:130px;
                height:auto;
                border:5px solid;
                margin-top:-70px;
                margin-left:50px;
                background: white;
                border-color:#0E78A0 !important;
            }
            .navbox{
                display:inline;
                background: black;
                width:150px;
                height:30px;
                color:white;
                text-decoration:none;
                font-size:20px;
                text-align:center;
                padding:0 10px;
                margin-right:5px;
            }
            .navbox:hover{
                opacity:0.7;
            }
            a:visited{
                color:white;
            }
            nav{
                margin-top:20px;
                margin-bottom:40px;
            }
            footer{
                position:absolute;
                margin-top:560px;
                margin-left:900px;
                color:white;
            }
            .head{
                font-size:90px;
                margin-top:-120px;
                margin-bottom:0;
                color:#6FC3C1;
            }
            .head2{
                font-size:90px;
                margin-top:-120px;
                margin-bottom:0;
                color:#77BF42;
            }
            body{
                width:700px;
                min-height:100%%;
                margin-left:auto;
                margin-right:auto;
                margin-top:100px;
            }
        </style>

    </head>
	<body>
		<div class="container">
            <h1 class="head">%s</h1>
			<nav>
				<div class="navbox">
					<a href="/">Home</a>
				</div>
				<div class="navbox">
					<a href="/recipes">Recipes</a>
				</div>
				<div class="navbox">
					<a href="/inventory">Inventory</a>
				</div>
				<div class="navbox">
					<a href="/liquor_types">Liquor types</a>
				</div>
           		<div class="navbox">
					<a href="/form">Forms</a>
				</div>
			</nav>
            <article>""" 
end = """ 	</article>

		</div>
		<img id="bottom" src="signituretrans.png" alt="signiture"/>
	</body>
</html>"""
class SimpleApp(object):
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')
        
        if (fn_name.isdigit()):
            num = int(fn_name)
            fn_name = "choose_form"

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        if(fn_name == "choose_form"):
            return fn(environ, start_response, num)
        else:
            return fn(environ, start_response)
            
    def index(self, environ, start_response):
        title = "Drinkz"
        content = """<p>Hi this Project 4 for CSE 491, hopefully you enjoy it :D</p>
        <input type="button" onclick="alertThem()" value="Show alert box">"""
        data = begining % (title,title) + content + end 
        #for the image in the bottom
        #pic = open('sp.png', 'rb').read()
        #data += pic
        #headers = [('Content-type','image/png'), ('Content-type', 'text/html')]

        start_response('200 OK', list(html_headers))
        #start_response('200 OK', headers)
        return [data] 

    def recipes(self, environ, start_response):
        title = "recipes"
        content = """<table border='1' margin='50px'>
        <tr>
        <td><strong>Recipes</strong></td>
        <td><strong>Available?</strong></td>
        </tr>
        """
        for k,v in db._recipes_db.iteritems():
            content += "<tr><td>%s</td><td> "%(k)
            if (v.need_ingredients):
                content += "no"
            else:
                content += "ya"
        content +=  "</td></tr>"
        content += "</table>"
        data = begining % (title,title) + content + end 
        start_response('200 OK', list(html_headers))
        return [data]
 
    def ajaxform(self, environ, start_response):
        title = "formAjax"
        os.chdir(r'/user/botrosma/cse491/cse491-drinkz/drinkz')
        content = open('ajaxform.html').read() 
        data = begining % (title,title) + content + end 
        start_response('200 OK', list(html_headers))
        return [content]

    def inventory(self, environ, start_response):
        title = "inventory"
        content = """<table border='1' margin='50px'>
        <tr>
        <td><strong>Manufacturer</strong></td>
        <td><strong>Liquor</strong></td>
        <td><strong>Amount</strong></td>
        </tr>
        """
        for k,v in db._inventory_db.iteritems():
            content += "<tr><td>%s </td><td>%s</td><td>%d ml\
            </td></tr>"%(k[0],k[1],v)
        content += "</table>"

        data = begining % (title,title) + content + end 
        start_response('200 OK', list(html_headers))
        return [data]

    def liquor_types(self, environ, start_response):
        title = "liquor"
        content = "<ul>"
        for (mfg, lqr,typ) in db._bottle_types_db:
            content += "<li>%s, %s, %s</li>"%(mfg,lqr,typ)
        content += "</ul>" 
        data = begining % (title,title) + content + end 
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def sp(self):
        content_type = 'image/png'
        data = open('signituretrans.png', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]
        
    def choose_form(self, environ, start_response, num):
        data = forms(num)

        start_response('200 OK', list(html_headers))
        return [data]

    def form(self, environ, start_response):
        title = "forms"
        content = """<p>Hi What would you like to do?</p>
        <p>Below you can see different forms, please choose one of them.</p>
        <nav>
        <div class="navbox" style='display:block;margin-bottom:20px'>
                <a href="/ml">Convert to ml</a>
            </div>
            <div class="navbox" style='display:block;margin-bottom:20px'>
                <a href="/lt">Insert Liquor</a>
            </div>
            <div class="navbox" style='display:block;margin-bottom:20px'>
                <a href="/in">Add to Inventory</a>
            </div>
            <div class="navbox" style='display:block;margin-bottom:20px'>
                <a href="/re">Add recipes</a>
            </div>
        </nav>
        """
        data = begining % (title,title) + content + end 

        start_response('200 OK', list(html_headers))
        return [data] 

    def recv_ml(self, environ, start_response):
        title = "ml form";
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        num = results['amount'][0]
        unit = results['unit'][0]
        if num.replace('.','',1).isdigit():
            amount = num + ' '+ unit
            r = db.convert_to_ml(amount)
            content_type = 'text/html'
            data = begining%(title,title) + "Amount: %.3f ml.  <a href='./'>return to index</a>" %(r)+ end
        else:
            data = "Please insert a valid value, which is a number. <a href='./'>return to index</a>" 

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_li(self, environ, start_response):
        title = "liquor form";

        #couldn't use jinja2 in begining because it is used in many
        #place and I would have to change all of them
        form = begining%(title,title) + """
        <form action='recv_li'>
        Manufacturer: <input type='text' name='mnf' size='10'>
        Liquor: <input type='text' name='liq' size='10'>
        Type: <input type='text' name='type' size='10'>
        <input type='submit'>
        </form>
        <br>
        """

        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        try:
            mnf = results['mnf'][0]
            liq = results['liq'][0]
            typ = results['type'][0]
            bulbError = False 
        except KeyError:
            error = "<p style='color:red'>Please make fill all the blanks</p>" 
            bulbError = True
            
        if (bulbError):
            pass
        else:
            error = ""
            db.add_bottle_type(mnf, liq, typ)

        content_type = 'text/html'

        cnt = """ 
        {% for typ in _bottle_types_db %}
             <li>{{ typ[0] }}, {{ typ[1] }}, {{ typ[2] }}</li>
        {% endfor %}
        </ul> 
        """

        lst = Environment().from_string(cnt).render( _bottle_types_db = db._bottle_types_db)

        data = form + error +"<ul>" + lst.encode('ascii','ignore') + end
        start_response('200 OK', list(html_headers))
        return [data]

    def recv_in(self, environ, start_response):
        title = "inv. form";

        #couldn't use jinja2 in begining because it is used in many
        #place and I would have to change all of them
        form = begining%(title,title) + """
        <form action='recv_in'>
        Manufacturer: <input type='text' name='mnf' size='10'>
        Liquor: <input type='text' name='liq' size='10'>
        Amount: <input type='text' name='amount' size='10'>
        unit: <select name="unit">
                <option value="oz"> oz</option>
                <option value="gallon">gallon</option>
                <option value="liter">liter</option>
            </select>
        <input type='submit'>
        </form>
        <br>
        """
        error = ""

        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        try:
            mnf = results['mnf'][0]
            liq = results['liq'][0]
            num = results['amount'][0]
            unit = results['unit'][0]
            bulbError =False 
        except KeyError:
            error = "<p style='color:red'>Please make fill all the blanks</p>" 
            bulbError = True
            
        if(bulbError):
            pass
        elif (not num.replace('.','',1).isdigit()):
            error = "<p style='text-color:red'>Please enter a number</p>" 
        else:
            amount = num + ' '+ unit
            ml_amount = db.convert_to_ml(amount)
            content_type = 'text/html'

            try:
                db.add_to_inventory(mnf, liq, amount)
            except db.LiquorMissing:
                error = " <p style='background:red'>Error: This liquor type is not found in our records, please add it in the liquor types form</p>"

        content_type = 'text/html'

        cnt = """ 
        <tr>
        <td><strong>Manufacturer</strong></td>
        <td><strong>Liquor</strong></td>
        <td><strong>Amount</strong></td>
        </tr>

        {% for key in inventory %}
             <tr>
             <td>{{ key[0] }}</td>
             <td>{{ key[1] }}</td>
             <td>{{ inventory[key] }} ml</td>
             </tr>
        {% endfor %}
        </table> 
        """

        lst = Environment().from_string(cnt).render( inventory = db._inventory_db)

        data = form + error +"<table border='1'  margin='50px'>" + lst.encode('ascii','ignore') + end
        start_response('200 OK', list(html_headers))
        return [data]

    def recv_re(self, environ, start_response):
        title = "recipe form";

        form =  """ 
        <form action='recv_re_2'>
            Name: <input type='text' name='name' size='10'>
			<br>
        {% for i in range( r[0] ) %}
            Comp. name: <input type='text' name='Compname' size='10'>
            Amount: <input type='text' name='amount' size='10'>
            unit: <select name="unit">
                    <option value="oz"> oz</option>
                    <option value="gallon">gallon</option>
                    <option value="liter">liter</option>
                </select>
        {% endfor %}
        {{ maxi }}
            <input type='submit'>
        </form>
        <br>
        """
        error = ""
        content_type = 'text/html'

        #parsing vars
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        #Here we check that they are not blank
        #If they are we print an error message
        try:
            n = results['num'][0]
            bulbError =False 
        except KeyError:
            error = "<p style='color:red'>Please make fill all the blanks<a href='\recv_re'>go back!</a></p>" 
            bulbError = True
           
        #Here we check that the number is a digit
        if(bulbError):
            pass
        elif (not n.replace('.','',1).isdigit()):
            error = "<p style='text-color:red'>Please enter a number <a href='\recv_re'>go back!</a></p>" 

        
        #here we render the jinja template
        frm = Environment().from_string(form).render(r= [int(n)])

        data = begining%(title,title) +error + frm.encode('ascii','ignore') + end
        start_response('200 OK', list(html_headers))
        return [data]
 
    def recv_re_2(self, environ, start_response):
        title = "recipe form";

        error = ""

        #parsing vars
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        try:
            name = results['name'][0]
            Compname = results['Compname']
            amnt = results['amount']
            unit = results['unit']
            bulbError =False 
        except KeyError:
            error = "<p style='color:red'>Please make fill all the blanks</p>" 
            bulbError = True

        if(bulbError):
            pass
        elif (not amnt[0].replace('.','',1).isdigit()):
            error = "<p style='text-color:red'>Please enter a number</p>" 
        else:
            totalA = []
            i = 0
            for a in amnt:
                amount = a + ' '+ unit[i]
                ml_amount = db.convert_to_ml(amount)
                content_type = 'text/html'
                m = '%.3f' %ml_amount + ' ' + 'ml'
                totalA.append(m)
                i += 1
            print 'totalA', totalA

        cmpt = []
        i = 0
        for c in Compname:
            cmpt.append((c,totalA[i]))
            i += 1

        print 'cmpt:',cmpt
        r = recipes.Recipe(name, cmpt)
        db.add_recipe(r)

        content_type = 'text/html'

        cnt = """ 
        <ul>
        {% for key in recipes %}
            <li> {{ key }} </li>
        {% endfor %}
        </ul> 
        """

        lst = Environment().from_string(cnt).render(recipes = db._recipes_db)
        
        data = begining%(title,title) +error + lst.encode('ascii','ignore') + end
            
        start_response('200 OK', list(html_headers))
        return [data]
     
    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        print environ
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_convert_units_to_ml(self,amount):
        return db.convert_to_ml(amount)
 
    def rpc_recipes_names(self):
        recp = ['hello']
        for k,v in db._recipes_db.iteritems():
            recp.append(k)

        return recp

    def rpc_liquor_inventory(self):
        inv = []
        for k,v in db._inventory_db.iteritems():
            inv.append(k)

        return inv

    def rpc_add_liquor_type(self,liquorT):
        #lqr = (maf,lqr,typ)
        #Check if they were empty
        bulbError = False 
        try:
            maf = liquorT[0]
            lqr = liquorT[1]
            typ = liquorT[2]
        except KeyError:
            bulbError = True
            
        if (bulbError):
            pass
        else:
            db.add_bottle_type(maf, lqr, typ)

        return (not bulbError)

    def rpc_add_to_inventory(self,bottle):
        error = "Added successfully"
        bulbError = False 
        #Check if they were empty
        try:
            maf = bottle[0]
            lqr = bottle[1]
            amnt = bottle[2]
        except KeyError:
            error = "Adding failed: make sure all required vars are given"
            bulbError = True
            
        if (bulbError):
            pass
        else:
            try:
                db.add_to_inventory(maf, lqr, amnt)
            except db.LiquorMissing:
                error = "Adding failed: the Liquor is missing, please add it to list of liquor types"
                bulbError = True

        return error 
 
    def rpc_add_recipe(self, name, compts):
        r = recipes.Recipe(name, compts)
        db.add_recipe(r)

        return True

def forms(C):
    #convert to ml
    if (C == 1):
        title = "ml form"
        os.chdir(r'/user/botrosma/cse491/cse491-drinkz/drinkz')
        content = open('ajaxform.html').read() 
        return begining%(title,title) + content +end 

    #This is for the liquor types
    elif (C == 2):
        title = "liquor form"
        return begining%(title,title) + """
        <form action='recv_li'>
        Manufacturer: <input type='text' name='mnf' size='10'>
        Liquor: <input type='text' name='liq' size='10'>
        Type: <input type='text' name='type' size='10'>
        <input type='submit'>
        </form>
        """ + end

    #This is for the inventory 
    elif (C == 3):
        title = "inventory form"
        return begining%(title,title) + """
        <form action='recv_in'>
        Manufacturer: <input type='text' name='mnf' size='10'>
        Liquor: <input type='text' name='liq' size='10'>
        Amount: <input type='text' name='amount' size='10'>
        unit: <select name="unit">
                <option value="oz"> oz</option>
                <option value="gallon">gallon</option>
                <option value="liter">liter</option>
            </select>
        <input type='submit'>
        </form>
        """ + end
   
    #This is for the reciepes 
    elif (C == 4):
        title = "recipe form"
        return begining%(title,title) + """
        <form action='recv_re'>
            Please enter the number of Components: <input type='text' name='num' size='10'>
            <input type='submit'>
        </form>
        """ + end

    else:
        return " "
    
