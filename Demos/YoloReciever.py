import socket
import time

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ClientSocket.connect(('localhost', 96385))

# Send data to the server (e.g., box coordinates and text)
Data = "100 100 50 50,Hello World"

ClientSocket.send(Data.encode('utf-8'))
time.sleep(3)
