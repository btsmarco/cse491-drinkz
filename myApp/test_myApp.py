import socket, sys, os

if len(sys.argv) != 3:
    print "Please enter the hostname, space, then a port"
    exit(0)
 
def T_Simple_GET():
    hostname = sys.argv[1]
    port = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname , int(port)))

    #asking the server for the index page
    s.send("GET / HTTP/1.0\r\n\r\n")
    
    reply = "" 
    #grabs pieces until there is no more info to grab
    while 1:
        buf = s.recv(100)
        if not buf:
            break 
        reply += buf

    assert reply.find("Hi there! This is my app"), t
    print reply
    sys.stdout.flush()
    s.close()

def T_GET_Form():
    hostname = sys.argv[1]
    port = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname , int(port)))

    #asking the server for the index page
    s.send("GET /form HTTP/1.0\r\n\r\n")
    
    s.send('I am good')

    reply = "" 
    #grabs pieces until there is no more info to grab
    while 1:
        buf = s.recv(100)
        if not buf:
           break 
        reply += buf

    print reply 

    sys.stdout.flush()
    s.close()

def T_GET_PIC():
    hostname = sys.argv[1]
    port = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname , int(port)))

    #asking the server for the index page
    s.send("GET /pic HTTP/1.0\r\n\r\n")
    
    reply = '' 
    buf = ''
    #grabs pieces until there is no more info to grab
    while 1:
        buf = s.recv(100)
        if not buf:
           break 
        if '\r\n' in buf:
            continue
        else:
            reply += buf
        
    pic = open('RSpartan-helmet.gif','wb')
    pic.write(reply)
    size = pic.tell()
    
    assert os.path.exists('Recieved-Spartan-helmet.gif')
    assert size == 2399, size

    pic.close

    #Test see if a file exsists and how many bytes does it have
    sys.stdout.flush()
    s.close()


if __name__ == "__main__":
    T_Simple_GET()
    T_GET_PIC()
    T_GET_Form()
