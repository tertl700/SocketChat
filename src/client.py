import socket

HEADER = 8
PORT = 17173
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    if msg != 'logout' or 'exit':
        message = msg.encode(FORMAT)
        msg_length = str(len(msg)).encode(FORMAT)
        msg_length += b' ' * (HEADER - len(msg_length))
        client.send(msg_length)
        client.send(message)
    print(client.recv(2048).decode(FORMAT))

print('Chat room client')
connected = True
while connected:
    msg = input()
    if msg == 'logout':
        connected = False
    send(msg)