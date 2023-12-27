import socket

s = socket.socket()

port = 12345

s.bind(('127.0.0.1', port))

print("Socket binded to %s" % (port))

s.listen(5)

print("Socket is listening")

while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    c.send('Thank you for connecting'.encode())
    c.close()
    break  # This should be inside the while loop
