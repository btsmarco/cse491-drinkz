#! /usr/bin/env python
from wsgiref.simple_server import make_server
import drinkz.db
from drinkz import recipes
import urlparse, simplejson

dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """\
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<p>
<img src='/helmet'>
"""
        start_response('200 OK', list(html_headers))
        return [data]
        
    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
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

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
    
def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
"""\
<style type="text/css"> 
            h2{
                color: #B0171F;
            }
            html, body{
                height:100%;
            }
            .main{
                background-image: url(../img/lamp.jpg);
                background-size:80%%;
            }
            .wrapper{
                width:auto;
            }
            .container{
                background:white;
                min-height:100%%;
                padding:30px 50px 50px 30px ;
                width:500px;
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
"""
