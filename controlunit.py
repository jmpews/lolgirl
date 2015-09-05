#-*-encoding:utf-8-*-
__author__ = 'jmpews'

import socket
import select
import queue
import time

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind(('localhost',9999))
server.listen(10)
inputs=[server]
outputs=[]

message_queues={}

while inputs:
    readable,writeable,exceptional=select.select(inputs,outputs,inputs)
    for s in readable:
        if s is server:
            connection,address=server.accept()
            print('connect from ',address)
            connection.setblocking(0)
            inputs.append(connection)
            # outputs.append(connection)
            message_queues[connection]=queue.Queue()
        else:
            data=s.recv(1024)
            # get一个job
            if data:
                print('recv',data,'from ',s.getpeername())
                if s not in outputs:
                    outputs.append(s)
            # 分布客户端异常
            else:
                print('closed from',s.getpeername())
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writeable:
        try:
            # 成功获得一个job
            s.send('success'.encode())
            outputs.remove(s)
        except queue.Empty as e:
            print(s.getpeername(),'queue empty')
            outputs.remove(s)

    for s in exceptional:
        print('exception on ',s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]