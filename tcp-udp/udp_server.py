import socket
import threading

clients = []

def listen():
    while True:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
        for c in clients:
            if c != addr:
                s.sendto(data, c)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 9999))

print("UDP Server started on port 9999...")

threading.Thread(target=listen, daemon=True).start()
