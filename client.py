import socket
import threading

def start_client() -> socket:
    client_object: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    ip_address = '127.0.0.1'
    port = 5555

    client_object.connect((ip_address,port))

    return client_object

def receive_messages(client_object: socket) -> None:
    while True:
        try:
            data = client_object.recv(1024)
            if not data:
                print("\nDisconnected from server.")
                break
            print(f"\n[Incoming]: {data.decode('utf-8')}")

        except:
            print("\nAn error occured. Disconnecting.")
            break

def send_messages(client_object: socket) -> None:
    while True:
        try:
            message = input("You: ")
            if message.lower() == "quit":
                break
            client_object.send(message.encode('utf-8'))
        
        except:
            print("\nAn error occured.")
            break

if __name__ == "__main__":
    client_object: socket  = start_client()

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_object,)
    )
    receive_thread.start()

    send_messages(client_object)
    client_object.close()
