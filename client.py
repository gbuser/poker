import socket
#HOST = "127.0.0.1"
PORT = 64444
HOST = (socket.gethostbyname("localhost"))
print(HOST)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    data = sock.recv(1024).decode()
    sock.sendall(b"Fuck you")
    sock.close()

print(f"received: {data}")