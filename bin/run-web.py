#! /usr/bin/env python
import socket, _mypath
from wsgiref.simple_server import make_server
from drinkz.app import SimpleApp
import simplejson

if __name__ == '__main__':
    port = 8999

    app = SimpleApp()

    httpd = make_server('',port,app)
    print "Serving on port %d....." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
            (socket.getfqdn(), port)
    httpd.serve_forever()
