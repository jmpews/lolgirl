__author__ = 'jmpews'
import socket

# server_address = ("112.126.76.80",9999)
server_address = ("127.0.0.1",9999)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(server_address)

sock.send('a:data'.encode())
# while True:
data = sock.recv(1024)
print(data)
sock.close()
