import socket
HOST = "127.0.0.1"
PORT = 64444
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    conn, addr = sock.accept()

    with conn:
        print(f"connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)