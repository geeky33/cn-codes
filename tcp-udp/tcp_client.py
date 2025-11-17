import socket
import threading

def recv_msg(s):
    while True:
        try:
            print(s.recv(1024).decode())
        except:
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9999))

threading.Thread(target=recv_msg, args=(s,), daemon=True).start()

while True:
    msg = input()
    s.send(msg.encode())
