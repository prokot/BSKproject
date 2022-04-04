import socket
from _thread import *
import threading as thrd
import gui
from main import App


class P2P:
    def __init__(self,app,bindPort) -> None:
        self.print_lock = thrd.Lock()
        self.isConnect = False
        self.connectPort = 0
        self.app = app
        self.host = "127.0.0.1"
        self.bindPort = int(bindPort)
        start_new_thread(self.sockets)


    def send(self,msg):
        self.socket.send(msg.encode('ascii'))

    def receive(self,c):
        while True:
            data = c.recv(1024)
            self.app.ui.writeMsg(data.decode('ascii'))
        c.close()
    
    def connect(self,port):
        self.connectPort = port
        self.isConnect = True
        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.connect((self.host,int(self.connectPort)))
        self.app.ui.writeMsg('Connected to :' + self.host +  " : " + str(self.connectPort) )
        self.socket = s2
        self.print_lock.acquire()
        start_new_thread(self.receive,(s2,))

    def sockets(self):

        

        s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        

        s1.bind((self.host,self.bindPort))
        self.app.ui.writeMsg("Listening on host :" + str(self.host) + " : " + str(self.bindPort))

        
        s1.listen(5)

        
        while True:
            if not self.isConnect:
                c,addr = s1.accept()
                self.app.ui.writeMsg('Connected to :' + addr[0] +  " : " + str(addr[1]) )
                self.socket = c
                self.print_lock.acquire()
                start_new_thread(self.receive,(c,))
        s1.close()

