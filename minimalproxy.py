import os,sys,thread,socket,argparse,time

#Args
parser = argparse.ArgumentParser(description='ProxyDescription')
parser.add_argument('port', action='store', help='Port Number', default=8080, type=int)
args = parser.parse_args()
#CONSTANT
BACKLOG = 8192  # max number of bytes we receive at once
BLOCKED = []

def main():
    port = args.port
    host = ''

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)

    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    # get the connection from client
    while True:
        conn, client_addr = s.accept()
        thread.start_new_thread(proxy, (conn, client_addr))
    s.close()

def printout(type,request,address):
    if "Block" in type or "Blacklist" in type:
        colornum = 91
    elif "Request" in type:
        colornum = 92


    print "\033[",colornum,"m",address[0],"\t",type,"\t",request,"\033[0m"

def proxy(conn, client_addr):
    # get the request from browser
    requestContent = conn.recv(BACKLOG)
    # parse the first line
    first_line = requestContent.split('\n')[0]

    # get url
    url = first_line.split(' ')[1].lower()

    # for i in range(0,len(BLOCKED)):
    #     if BLOCKED[i] in url:
    #         printout("Blacklisted",first_line,client_addr)
    #         conn.close()
    #         sys.exit(1)


    printout("Request",first_line,client_addr)

    # find the webserver and port
    http_pos = url.find("://")          # find pos of ://
    temp = url[(http_pos+3):]       # get the rest of url

    #port_pos = temp.find(":")           # find the port pos (if any)

    # find end of web server
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)


    # if (port_pos==-1 or webserver_pos < port_pos):      # default port

    outAddress = temp[:webserver_pos]
    # else:       # specific port
    #
    #     webserver = temp[:port_pos]
    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((outAddress, 80))
        s.send(requestContent)         # send request to webserver

        while True:
            # receive data from web server
            data = s.recv(BACKLOG)
            if (len(data) > 0):
                # send to browser
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        printout("Peer Reset",first_line,client_addr)
        sys.exit(1)


main()
