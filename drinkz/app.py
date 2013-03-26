#! /usr/bin/env python
from wsgiref.simple_server import make_server

class SimpleApp(object):
    def __call__(self, environ, start_response):
        status = '200 OK' #a status passed to the start_response

        #environ is a dictionary of CGI-style variables
        #PATH_INFO is everything after the port in the url.
        path = environ['PATH_INFO'] 
        fp = open('environ','w')

        if path == '/':
            content_type = 'text/html'
            data = """\
Check out:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>
<a href='environ'>environ</a>
"""
        elif path == '/content':
            content_type = 'text/html'
            data = open('somefile.html').read()
        elif path == '/error':
            status = "404 Not Found"
            content_type = 'text/html'
            data = "Couldn't find your stuff."
        elif path == '/helmet':
            content_type = 'image/gif'
            data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()
        elif path == '/environ':
            content_type = 'text/plain'
            data = open('environ').read()
        else:
            content_type = 'text/plain'
            data = "Hello, world; got path request %s" % environ['PATH_INFO']
       
       #THis is the second variable passed to start_response and  
       #is a list of tuples, first one defines content-type 
        headers = [('Content-type', content_type)]
        start_response(status, headers)
        
        #the method always has to return the data
        return [data]

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    port = 8999 #after each time you have to kill the process to use the port again
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.gethostname(), port)
    httpd.serve_forever()
