import socket

# Client configuration
HOST = '192.168.1.100'  # Replace with Pepper's IP address
PORT = 12345            # Must match the server's port

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    # Send data to the server
    message = "Hello, Pepper!"
    client_socket.sendall(message.encode('utf-8'))
    print("Message sent:", message)
    
    # Receive the response from the server
    response = client_socket.recv(1024)
    print("Response from server:", response)
    
    client_socket.close()

if _name_ == "_main_":
    start_client()
