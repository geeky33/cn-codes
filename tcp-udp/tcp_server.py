import socket
import threading

clients = []

def handle_client(conn):
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            for c in clients:
                if c != conn:
                    c.send(msg)
        except:
            break

    conn.close()
    clients.remove(conn)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen()

print("TCP Server started on port 9999...")

while True:
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn,)).start()
