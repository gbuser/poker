import socket
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'


SERVER = '127.0.0.1'
#SERVER = '157.230.183.234'
addr = (SERVER, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(addr)

def send(msg):
    message = msg.encode((FORMAT))
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sock.send(send_length)
    sock.send(message)


send("fuck you and the horse you came in on")

print(sock.recv(2048).decode(FORMAT))
print(sock.recv(2048).decode(FORMAT))
print(sock.recv(2048).decode(FORMAT))
print(sock.recv(2048).decode(FORMAT))

send(DISCONNECT)