__author__ = 'jmpews'
import socket

messages = ["This is the message" ,
            "It will be sent" ,
            "in parts "]

print("Connect to the server")

# server_address = ("112.126.76.80",10001)
server_address = ("127.0.0.1",9999)


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(server_address)

sock.send('a:data'.encode())
data = sock.recv(1024)
sock.close()
