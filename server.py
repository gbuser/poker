import socket
import threading
SERVER = ""
PORT = 5050
ADDR = (SERVER, PORT)
HEADER = 64
DISCONNECT = "!DISCONNECT"
FORMAT = 'utf-8'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)


def start():
    sock.listen()
    print(f'Server is listening on {SERVER}, port {PORT}')
    while 1:
        conn, addr = sock.accept()
        thread = threading.Thread(target= handle_client, args = (conn, addr))
        thread.start()
        print(f'active threads: {threading.active_count() - 1}')

def handle_client(conn, addr):
    print(f'connected to {addr}')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')
            print(f'{addr}: {msg}')
            conn.send("You are connected to basic poker server".encode(FORMAT))
            conn.send("care to play some poker?".encode(FORMAT))
            if msg == DISCONNECT:
                connected = False
                conn.close()

print("starting server")
start()
