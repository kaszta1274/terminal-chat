import socket
import threading

from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.key_binding import KeyBindings

chat_log = TextArea(prompt="---- Chat Started ----\n", read_only=True, scrollbar=True)
message_input = TextArea(prompt="Message: ", multiline=False)

root_container = HSplit([
    chat_log,
    Window(height=1, char="-", style="class:line"),
    message_input
])
layout = Layout(root_container, focused_element=message_input)

kb = KeyBindings()

@kb.add("c-c")
def _(event):
    app.exit()

app = Application(layout=layout, key_bindings=kb, full_screen=True)

def append_to_log(text: str) -> None:
    chat_log.text += f"\n{text}"
    chat_log.control.move_cursor_down()
    app.invalidate()

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
                if app.is_running:
                    app.loop.call_soon_threadsafe(append_to_log, "\nDisconnected from server.")
                break

            if app.is_running:
                app.loop.call_soon_threadsafe(append_to_log, f"{data.decode('utf-8')}")

        except Exception as e:
            if app.is_running:
                app.loop.call_soon_threadsafe(append_to_log, f"\nAn error occured. Disconnecting: {e}")
            break

def send_messages(client_object: socket, client_id: str) -> None:
    def handler(buffer):
        try:
            message = message_input.text.strip()
            if not message:
                return

            append_to_log(f"You: {message}")
            
            payload = f"{client_id}: {payload}"
            client_object.send(payload.encode('utf-8'))
            message_input.text = ""
        
        except Exception as e:
            append_to_log(f"\nError while sending a message: {e}")
    return handler

if __name__ == "__main__":
    client_object: socket  = start_client()

    welcome_text = "---- Connected to the server ----\n---- To exit press CTRL + C ----"
    print(welcome_text)
    client_id = input("To start chatting, please assign your name: ")

    message_input.accept_handler = send_messages(client_object, client_id)
    
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_object,),
        daemon=True
    )
    receive_thread.start()

    app.run()

    try: 
        client_object.send(f"{client_id} has left the chat".encode('utf-8'))
        client_object.shutdown(socket.SHUT_RDWR)
    except Exception:
        pass
    
    client_object.close()
    print("Connection closed")
