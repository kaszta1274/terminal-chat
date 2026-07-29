import socket
import random
import string

def start_server() -> socket:
    server_object: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ip_address = '127.0.0.1'
    port = 5555
    server_object.bind((ip_address, port))

    return server_object
    
def server_listen(server_object: socket) -> None:
    server_object.listen()
    
    connection_object, _ = server_object.accept()
    
    if connection_object:
        print("SERVER CONNECTED TO CLIENT")
    
        connection_object.send(b"type the messege")
    
        data_receive = connection_object.recv(1024)
    
        while data_receive != b"stop":
            print("{}: {}".format("CLIENT MESSAGE: ", data_receive.decode('utf-8')))
            server_input = random.choice(string.ascii_letters)
            connection_object.send(server_input.encode('utf-8'))
            data_receive = connection_object.recv(1024)

if __name__ == "__main__":
    server_object: socket  = start_server()
    server_listen(server_object)