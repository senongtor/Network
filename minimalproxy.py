import os,sys,thread,socket,time, argparse

#Args
parser = argparse.ArgumentParser(description='ProxyDescription')
parser.add_argument('port', action='store', help='Port Number', default=8080, type=int)
args = parser.parse_args()

MAX_DATA_RECV = 8192
BLOCKED = ['www.baidu.com','www.cnn.com','www.nyu.edu','www.aol.com','www.dmv.org',
'www.stackoverflow.com','www.bbc.co.uk','www.youku.com','www.ticketmaster.com','www.columbia.edu']
FILTERED = ['research']

def main():
    port=args.port
    #Accecpt all hosts
    host = ''

    print 'Proxy Server Running on port ',port

    try:
        #create a socket with the proxy
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        s.close()
        s = None
        print 'Could not open socket:', msg[1]
        sys.exit(1)

    while True:
        conn, client = s.accept()
        thread.start_new_thread(proxy_process, (conn, client))
    s.close()


def proxy_process(conn, client):
    #read the request
    request = conn.recv(MAX_DATA_RECV)
    print "RRR",request
    if request == '':
        conn.close()
        return

    #Read the first line of the request, it will contains GET http://...
    header = request.split('\n')[0]
    url = header.split(' ')[1].lower()

    if '://' in url:
        httptype=url.split('://')[0]
        url=url.split('://')[1]

    port = 80
    # if httptype=='https':
    #     port = 443
    
    if ':' in url:
        port=url.split(':')[1]
        url=url.split(':')[0]

    if '/' in url:
        url = url[:url.find('/')]

    if url not in BLOCKED:
        print "\033[",92,"m","\t","Request","\t",header,"\033[0m"

    try:
        # create a socket to connect to the destination
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((url, port))
        s.send(request)

        while True:
            data = ''
            if url in BLOCKED:
                data=r'''HTTP/1.0 404 Not Found
                Content-Type: text/html

                404 NOT FOUND!

                '''
                conn.send(data)

                print "\033[",91,"m","HTTP/1.0 404 Not Found For ", url,"\033[0m"
                break

            data=s.recv(MAX_DATA_RECV)

            if (len(data) > 0):
                if FILTERED[0] in data.lower():
                    data=r'''HTTP/1.0 404 Not Found
                    Content-Type: text/html

                    404 NOT FOUND!

                    '''
                    conn.send(data)
                    s.close()
                    conn.close()
                # send to client
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error as msg:
        s.close()
        conn.close()
        sys.exit(1)

main()
