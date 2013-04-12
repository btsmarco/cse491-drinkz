#from wsgiref.simple_server import make_server
import urlparse, simplejson
from jinja2 import Environment  
from urllib2 import urlopen
from json import load


begining = """ \
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
        <title> %s </title>
    </head>
	<body>
		<div class="container">
            <h1 class="head">%s</h1>
            <article>""" 
end = """ 	</article>
		</div>
	</body>
</html>"""

class MyApp(object):
    def __call__(self, environ, start_response):
        status = '200 OK'

        path = environ['PATH_INFO']
        data = ""
        title = "MY APP"
        content = " "

        if path == '/':
            content_type = 'text/html'
            title = "MY APP"
            content = """<p>Hi there!This is my app, hopefully you  will like it:D</p><br><a href='/form'> go to the form </a><br><a href='/pic'>Get that pic </a><br>"""

            data = begining % (title,title) + content + end 
        elif path == '/form':
            content_type = 'text/html'
            title = "form"
            content = """
            <form action='recv'>
            How are you doing today? <input type='text' size='30' name='in'> <input type='submit'></form>"""

            data = begining % (title,title) + content + end 
        elif path == '/recv':
            content_type = 'text/html'
            title = 'form'
            content= """You entered=%s, See yah"""
            response = environ['QUERY_STRING']
            results = urlparse.parse_qs(response)

            resp = results['in']
            
            data = begining % (title,title) + content%resp[0] + end 
        elif path == '/pic':
            content_type = 'image/gif'
            data = open('Spartan-helmet.gif','rb').read()
            
        else:
            content_type = 'text/plain'
            data = 'Hello Sir, got path request %s' % environ['PATH_INFO']
        headers = [('Content-type', content_type)]
        start_response('200 OK', headers)

        return [data]



