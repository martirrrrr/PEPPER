import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all available IP addresses
PORT = 5000       # Port to listen on

# Create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is listening on port {}".format(PORT))

try:
    while True:
        # Accept connections from the client
        conn, addr = server_socket.accept()
        print("Connection accepted from: {}".format(addr))
        
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break
        print("Data received: {}".format(data))
        
        # Send a response back to the client
        response = "Data received successfully"
        conn.send(response)

        conn.close()
except KeyboardInterrupt:
    print("Server terminated manually.")
finally:
    server_socket.close()
