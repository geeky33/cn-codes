import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))  # Bind to any available port

server = ('localhost', 9999)

def recv_msg():
    while True:
        try:
            data, _ = s.recvfrom(1024)
            print(data.decode())
        except:
            break

threading.Thread(target=recv_msg, daemon=True).start()

while True:
    msg = input()
    s.sendto(msg.encode(), server)
