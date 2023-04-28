import socket
import cv2

# create a socket object
Socket = socket.socket()

# get the local machine name
Host = Socket.gethostname()

# connect to the server
Socket.connect((Host, 96385))

# send data to the server
Socket.send("Hello, server!".encode())

# close the socket
Socket.close()
