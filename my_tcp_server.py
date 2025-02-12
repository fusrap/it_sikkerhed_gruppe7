from socket import AF_INET, SOCK_STREAM, socket
import re
from datetime import datetime


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


def serverSetup(port: int): 
    """
    Opsætning af serveren socket
    TCP = SOCK_STREAM
    AF_INET = IPv4
    """
    server_port = port
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',server_port))
    server_socket.listen(1)
    print("The server is ready to receive")
    return server_socket

def createResponse(url:str):
    """
    Modtager en URL fra http request lines og returnere status+side.
    Hvis siden ikke fundes returneres 404+PAGE_NOT_FOUND. 

    """
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
    """
    input eksempel: request_line = ["GET", "/index.html", "HTTP/1.1"]
    Denne metode tjekker om den først linje i request er valid.
    Hvis alkle felter er valide returneres: method, url, version.
    """
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
    """
    Denne metoder modtager alle resterne header, som bliver sent i et Key: value format.
    Eksempel på andre headers: headers = ['Host: localhost', 'Connection: keep-alive', 'Cache-Control: max-age=0'....]
    De samles og retuneres i en dict {}.
    """
    header_dict = {}
    for header in headers:
        if ': ' in header:
            key, value = header.split(': ', 1)
            header_dict[key] = value
    return header_dict, None  

"""
Validere om et request er valid og opdelere requestet i et dict efter:
    request_dict = {
        'METHOD': method,
        'URL': url,
        'HTTP_VERSION': version,
        'HEADERS': headers_lines,
        'BODY': body
    }
"""
def handleRequest(request: str):
    headers_lines = request.split('\r\n')

    if not headers_lines or headers_lines[0].strip() == '':
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

def logResponse(response, response_size,client_address,request_dict):
    """
    Opretter en log fil og logger.
    """
    with open("log.txt", "a") as file:
        method = request_dict["METHOD"]
        version = request_dict["HTTP_VERSION"]
        url = request_dict["URL"]
        code = response.split()[1]
        client_ip = client_address[0]
        timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")
        
        file.write(f'{client_ip} - - [{timestamp}] "{method} {url} {version}" {code} {response_size}\n')
     

server = serverSetup(80)
while True:
    conn_socket,client_address = server.accept()
    request = conn_socket.recv(2048).decode()
    
    try:
        request_dict = handleRequest(request)
        print('Request DEBUG', request_dict)
        
        response = createResponse(request_dict["URL"])
        response_packet = response.encode()
        response_size = len(response_packet)
        
        logResponse(response, response_size, client_address, request_dict)
        response_packet = response.encode()
        
        conn_socket.send(response_packet)
        
    except Exception as error:
        print(error)
        conn_socket.send((RESPONSE_400_BAD_REQUEST).encode())     
        logResponse(RESPONSE_400_BAD_REQUEST,response_size,client_address,{'METHOD':None,'HTTP_VERSION':None,'URL':None,})           
    
    print("connection received from {}:{}".format(client_address[0],client_address[1]))
    print('RAW_RQUEST: ', request)