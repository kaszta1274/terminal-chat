import socket

def start_client() -> socket:
    client_object: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    ip_address = '127.0.0.1'
    port = 5555

    client_object.connect((ip_address,port))

    return client_object

def client_listen(client_object: socket) -> None:
    data_receive = client_object.recv(1024)

    if data_receive:
        print("CLIENT CONNECTED TO SERVER")
        print(data_receive.decode('utf-8'))

        while data_receive:
            client_input = input().encode('utf-8')

            client_object.send(client_input)

            data_receive = client_object.recv(1024)
            if data_receive:
                print("{}: {}".format("SERVER", data_receive.decode('utf-8')))

if __name__ == "__main__":
    client_object: socket  = start_client()
    client_listen(client_object)