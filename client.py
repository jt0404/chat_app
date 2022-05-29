import socket 
import threading

nickname = input('Choose a nickname: ')

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'Nickname: ':
                client.send(nickname.encode('utf-8')) 
            else:
                print(message)
        except Exception as e:
            print('[EXCEPTION]:', e)
            client.close()
            break

def send_message():
    while True:
        message = f'{nickname}: {input()}'
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    send_thread = threading.Thread(target=send_message)
    send_thread.start()
