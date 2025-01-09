import socket

# Client configuration
SERVER_IP = '192.168.1.104'  # Pepper's IP address
SERVER_PORT = 5000           # Port Pepper is listening on

# Create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to Pepper at {}:{}".format(SERVER_IP, SERVER_PORT))

    # Send data to the server
    message = "Hello, Pepper!"
    client_socket.send(message)
    print("Message sent: {}".format(message))

    # Receive response from the server
    response = client_socket.recv(1024)
    print("Response from server: {}".format(response))

except Exception as e:
    print("Error: {}".format(e))
finally:
    client_socket.close()
