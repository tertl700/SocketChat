import socket
import re

FORMAT = 'utf-8'
HEADER = 8
PORT = 17173
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
users = {}

def update_users():
    #reading users from file
    with open('../users.txt') as f:
        for line in f:
            line = re.sub('[(){}<>]', '', line)
            (key, val) = line.strip().split(', ')
            users[key] = val


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(conn, addr, user):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            split_msg = msg.split()
            # check for logout command and disconnect
            if msg == 'logout':
                print(f'{user} logout')
                connected = False
                conn.send(f'Server: {user} left'.encode(FORMAT))
            # check for send command and properly send message
            elif split_msg and split_msg[0] == 'send': 
                message = msg.replace('send ', '')
                print(f'{user}: {message}')
                conn.send(f'{user}: {message}'.encode(FORMAT))
            else:
                conn.send('Please use commands "send" or "logout"'.encode(FORMAT))
                continue
    #conn.close()

def login(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
            # get length of incoming message and split into list
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            split_msg = msg.split()
            
            # check for login command in correct format
            if len(split_msg) == 3 and split_msg[0] == 'login':
                if split_msg[1] in users and users.get(split_msg[1]) == split_msg[2]:
                    print(f'{split_msg[1]} login.')
                    conn.send(f'Server: {split_msg[1]} joins'.encode(FORMAT))
                    send(conn, addr, split_msg[1])
                    connected = False
                else:
                    conn.send('Incorrect username or password'.encode(FORMAT))
            
            # check for newuser command in correct format        
            elif len(split_msg) == 3 and split_msg[0] == 'newuser':
                if split_msg[1] in users:
                    conn.send(f'{split_msg[1]} is already a user'.encode(FORMAT))
                elif len(split_msg[1]) > 32:
                    conn.send('UserID must be below 32 characters'.encode(FORMAT))
                elif len(split_msg[2]) < 4 or len(split_msg[2]) > 8:
                    conn.send('Password must be between 4 and 8 characters'.encode(FORMAT))
                else: #add user to file and reread file
                    with open('../users.txt', 'a') as f:
                        f.write(f'\n({split_msg[1]}, {split_msg[2]})')
                    conn.send(f'User {split_msg[1]} successfully created'.encode(FORMAT))
                    update_users()
            # check for logout command and disconnect
            elif split_msg and split_msg[0] == 'logout':
                connected = False
            else:
                conn.send('Server: Denied. Please login first'.encode(FORMAT))
    
    conn.close()
            


def start():
    update_users()
    server.listen()
    while True:
        conn, addr = server.accept()
        login(conn, addr)

print('Chat room server')
start()

