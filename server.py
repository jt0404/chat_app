import threading
import socket

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_clients(client):
    print('[SERVER]: Started')
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            print('[EXCEPTION]:', e)
            index = clients.index(client)
            clients.pop(index)
            nickname = nicknames.pop(index)
            broadcast(f'{nickname} has left the chat'.encode('utf-8'))
            client.close()
            break

def accept_connections():
    while True:
        client, address = server.accept()
        print(f'[SERVER]: New connection: {address}')

        client.send('Nickname: '.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'[SERVER]: Nickname of the client is: {nickname}')
        broadcast(f'{nickname} has joined the chat!'.encode('utf-8'))
        client.send('Connected to the server'.encode('utf-8'))

        thread = threading.Thread(target=handle_clients, args=(client, ))
        thread.start()

if __name__ == "__main__":
    accept_connections()
