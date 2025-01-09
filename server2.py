import socket

# Configurazione del server
HOST = '0.0.0.0'  # Ascolta su tutte le interfacce di rete
PORT = 12345      # Porta su cui ascoltare

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)  # Ascolta una connessione alla volta
    print("Server in ascolto su {}:{}".format(HOST, PORT))
    
    try:
        while True:
            conn, addr = server_socket.accept()
            print("Connesso da:", addr)
            
            # Riceve e stampa i dati
            data = conn.recv(1024)
            if not data:
                break
            print("Dati ricevuti:", data)
            
            # Invia una risposta al client
            conn.sendall(b"Ricevuto: " + data)
            conn.close()
    except KeyboardInterrupt:
        print("Chiusura del server...")
    finally:
        server_socket.close()

if _name_ == "_main_":
    start_server()
