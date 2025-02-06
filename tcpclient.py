#!/usr/bin/python3

from socket import *

server_name = "localhost"
server_port = 80

while True:
    print("\nSelect HTTP request type:")
    print("1 - GET /")
    print("2 - GET /home")
    print("3 - GET /myPage")
    print("4 - Malformed HTTP request")
    print("q - Quit")

    choice = input("Enter your choice (1-4 or q): ").strip().lower()

    if choice == "q":
        print("Exiting...")
        break

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
    elif choice == "4":
        # Missing Host header (malformed request)
        request = (
            "GET /badrequest HTTP/1.1\r\n"
            "\r\n"
        )
    else:
        print("Invalid choice. Using default request (GET /).")
        request = (
            "GET / HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "\r\n"
        )

    # Create a new socket for each request
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((server_name, server_port))
        client_socket.sendall(request.encode())

        response = client_socket.recv(4096)
        print("\nFrom server:\n", response.decode(errors="replace"))
    except Exception as e:
        print(f"Error communicating with the server: {e}")
    finally:
        client_socket.close()
