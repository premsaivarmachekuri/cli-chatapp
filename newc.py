import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nickname = input("Choose your nickname: ")

port = 7976

client.connect(('127.0.0.1', port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            client.close()
            break


def write():
    while True:
        message = '{}'.format(nickname)
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

write_thread = threading.Thread(target=write, daemon=True)
write_thread.start()
