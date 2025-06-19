import socket

def handle_request(client_socket, request_data):
    """
    Handles an incoming client request and sends an appropriate HTTP response.

    Args:
        client_socket (socket.socket): The client socket object.
        request_data (str): The decoded request data from the client.
    """
    if "GET /admin" in request_data:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nWelcome to the admin page!"
    else:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, this is a simple web server!"
    
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def main():
    """
    Main function to set up and run a simple web server.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)

    print("Server listening on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        request_data = client_socket.recv(1024).decode('utf-8')
        handle_request(client_socket, request_data)

if __name__ == "__main__":
    main()