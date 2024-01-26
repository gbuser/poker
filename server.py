import socket
import threading
from poker_utils import *
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
            conn.send("care to play some poker?".encode(FORMAT))
            conn.send("you've been dealt:\n".encode(FORMAT))
            deck = make_deck()
            random.shuffle(deck)
            hand = deal_cards(5, deck)
            hand = sort_hand(hand)
            #msg = str(data[hand]['tier0'])
            conn.send(string_hand(hand).encode(FORMAT))
            conn.send("test".encode(FORMAT))
            #print(msg)
            #conn.send(msg.encode(FORMAT))
            if msg == DISCONNECT:
                connected = False
                conn.close()

print("starting server")
start()
