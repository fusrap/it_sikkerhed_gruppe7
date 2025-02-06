#!/usr/bin/python3

from socket import *

server_name = "localhost"
server_port = 80

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect((server_name, server_port))

print("Select HTTP request type:")
print("1 - GET /")
print("2 - GET /home")
print("3 - GET /myPage")
print("4 - Malformed HTTP request")

choice = input("Enter your choice (1-4): ")

if choice == "1":
    request = (
        "GET / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )
elif choice == "2":
    request = (
        "GET /home HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )
elif choice == "3":
    request = (
        "GET /myPage HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )
# missing Host header
elif choice == "4":
    request = (
        "GET /badrequest HTTP/1.1\r\n"
        "\r\n"
    )
else:
    request = (
        "GET / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )

client_socket.sendall(request.encode())

response = client_socket.recv(4096)
print("From server:\n", response.decode(errors="replace"))

client_socket.close()
