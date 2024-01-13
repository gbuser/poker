import socket
HOST = "127.0.0.1"
PORT = 64444
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'socket created host: {HOST}  port: {PORT}')
except: "could not create socket"

try:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print("socket is listening")
except:
    print("could not bind/listen")

while 1:
    conn, addr = sock.accept()
    print(f'Received connection from {addr}. Connection = {conn} ')
    conn.send("go on, fuck yourself".encode())
    data = conn.recv(1024).decode()
    print(f'Received: {data}')
print("end of program")
