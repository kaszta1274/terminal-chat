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
            print(f"\n{data.decode('utf-8')}")

        except Exception as e:
            print(f"\nAn error occured. Disconnecting. Error: {e}")
            break

def send_messages(client_object: socket, client_id: str) -> None:
    while True:
        try:
            message = input("You: ")
            message = f"{client_id}: {message}"
            client_object.send(message.encode('utf-8'))
        
        except Exception as e:
            print(f"\nError while sending a message: {e}")
            break

if __name__ == "__main__":
    client_object: socket  = start_client()

    welcome_text = "---- Connected to the server ----\n---- To exit press CTRL + C ----"
    print(welcome_text)

    client_id = input("To start chatting, please assign your name: ")

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_object,)
    )
    receive_thread.start()

    try:
        send_messages(client_object, client_id)

    except KeyboardInterrupt:
        print("\nYou have left the chat")
        client_object.send(f"{client_id} has left the chat".encode('utf-8'))

    client_object.close()
    print("Connection closed")
