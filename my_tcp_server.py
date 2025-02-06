from socket import AF_INET, SOCK_STREAM, socket
import re


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
    

def splitRequestLine(request_line):
    if len(request_line) < 3:
        raise ValueError(f"Invalid HTTP request line: {' '.join(request_line)}")

    method = request_line[0]
    if method not in {'GET'}:
        raise ValueError(f"Invalid HTTP request line: {method}")
    
    url = request_line[1]
    if not re.findall(r"/[A-Za-z0-9_-]*", url):
        raise ValueError(f"Invalid HTTP request line: {url}")
    
    version = request_line[2]
    if version not in {"HTTP/1.1", "HTTP/1.0"}:
        raise ValueError(f"Invalid HTTP request line: {version}")
    
    return method, url, version

def splitHeader(headers: list):
    header_dict = {}
    for header in headers:
        if ': ' in header:
            key, value = header.split(': ', 1)
            header_dict[key] = value
    return header_dict, None  

def handleRequest(request: str):
    headers_lines = request.split('\r\n')

    if not headers_lines or len(headers_lines) < 1 or headers_lines[0].strip() == '':
        raise ValueError("Received an empty or malformed HTTP request")

    request_line = headers_lines[0].split()
    method, url, version = splitRequestLine(request_line)

    headers_lines, body = splitHeader(headers_lines[1:])
    
    if version == 'HTTP/1.1':
        if headers_lines.get("Host", None) == None:
            raise ValueError("Received an empty or malformed HTTP request")      
        
    request_dict = {
        'METHOD': method,
        'URL': url,
        'HTTP_VERSION': version,
        'HEADERS': headers_lines,
        'BODY': body
    }
    return request_dict

server = serverSetup(80)
while True:
    conn_socket,client_address = server.accept()
    request = conn_socket.recv(2048).decode()
    
    # validate request
    try:
        request_dict = handleRequest(request)
        print('Request DEBUG', request_dict)
        conn_socket.send(routing(request_dict["URL"]).encode())
    except Exception as error:
        print(error)
        conn_socket.send((RESPONSE_400_BAD_REQUEST).encode())                
    
    print("connection received from {}:{}".format(client_address[0],client_address[1]))
    print('RAW_RQUEST: ', request)

    # try:
    #     headers = makeHeaderDict(request)
    # except IndexError:
    #     conn_socket.send((RESPONSE_400_BAD_REQUEST+PAGE_NOT_FOUND).encode())
        
    # logging
    

server_socket.close()
conn_socket.close()