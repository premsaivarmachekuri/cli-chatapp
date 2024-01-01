import socket
import threading

host = '127.0.0.1'
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []


def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))


def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break 


print("Server listening on", host, ":", port)

def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{}joined!".format(nickname))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()