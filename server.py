import socket
import threading

active_clients = []

def start_server() -> socket:
    server_object: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ip_address = '127.0.0.1'
    port = 5555
    server_object.bind((ip_address, port))

    return server_object
    
def server_listen(server_object: socket) -> None:
    server_object.listen()
    print("Server is listening for incoming connections...")

    while True:
        connection_object, client_address = server_object.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]} established!")

        client_thread = threading.Thread(
            target=handle_client,
            args=(connection_object,)
        )

        client_thread.start()

def handle_client(connection_object: socket) -> None:
    active_clients.append(connection_object)

    while True:
        try:
            data = connection_object.recv(1024)
            if not data:
                break

            for client in active_clients:
                if client != connection_object:
                    client.send(data)
        except Exception as e:
            print(f"\nError while handling client's message: {e}") 
            break

    active_clients.remove(connection_object)
    connection_object.close()

if __name__ == "__main__":
    server_object: socket  = start_server()

    try:
        server_listen(server_object)
        
    except KeyboardInterrupt:
        message = "\nServer shutting down..."
        print(message)
        for client in active_clients:
            client.send(message.encode('utf-8'))
            client.close()
        server_object.close()
