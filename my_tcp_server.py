from socket import AF_INET, SOCK_STREAM, socket

RESPONSE_404_NOT_FOUND_HEADER = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n'
RESPONSE_400_BAD_REQUEST = 'HTTP/1.1 400 BAD REQUEST\r\n'
RESPONSE_200_OK_HEADER = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n'
RESPONSE_301_MOVED_PERMANENTLY_HEADER = 'HTTP/1.1 301 Moved Permanently\r\nLocation: https://cdn-icons-png.flaticon.com/512/4784/4784738.png\r\n\r\n'


with open('404.html', 'r', encoding='utf-8') as notFoundPage:
    PAGE_NOT_FOUND = notFoundPage.read()

with open('index.html', 'r', encoding='utf-8') as indexPage:
    PAGE_HOME = indexPage.read()

with open('my_page.html', 'r', encoding='utf-8') as myPage:
    MY_PAGE = myPage.read()

RESPONSE_404_NOT_FOUND_RESPONSE = RESPONSE_404_NOT_FOUND_HEADER + PAGE_NOT_FOUND


def makeHeaderDict(request: str):
    requestHeaders = request.split()
    headerDict = {}
    headerDict['METHOD'] = requestHeaders[0]
    headerDict['URL'] = requestHeaders[1]
    headerDict['VERSION'] = requestHeaders[2]
    return headerDict

def serverSetup(port: int): 
    server_port = port
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',server_port))
    server_socket.listen(1)
    print("The server is ready to receive")
    return server_socket

def routing(url:str):
    try:
        routes = {
            '/': RESPONSE_200_OK_HEADER + PAGE_HOME,
            '/home': RESPONSE_200_OK_HEADER + PAGE_HOME,
            '/myPage': RESPONSE_200_OK_HEADER + MY_PAGE,
            '/favicon.ico': RESPONSE_301_MOVED_PERMANENTLY_HEADER
        } 
        return routes[url]
    except:
        return RESPONSE_404_NOT_FOUND_RESPONSE



server = serverSetup(80)
while True:
    conn_socket,client_address = server.accept()
    request = conn_socket.recv(2048).decode()
    print("connection received from {}:{}".format(client_address[0],client_address[1]))
    print('RAW_RQUEST: ', request)

    try:
        headers = makeHeaderDict(request)
        conn_socket.send(routing(headers['URL']).encode())
    except IndexError:
        conn_socket.send((RESPONSE_400_BAD_REQUEST+PAGE_NOT_FOUND).encode())

server_socket.close()
conn_socket.close()