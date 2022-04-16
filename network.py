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
        self.pubKey = 0
        start_new_thread(self.sockets)


    def send(self,msg):
        data = self.app.crypto.decryptData(self.app.crypto.encryptData(msg.encode('ascii')))
        self.socket.send(msg.encode('ascii'))

    def receive(self,c):
        #self.pubKey = c.recv(512)

        while True:
            data = c.recv(1024)
                
            self.app.ui.writeMsg(data.decode('ascii'))
        c.close()
    
    def connect(self,port):
        self.connectPort = port
        self.isConnect = True
        
        socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM).connect( (self.host, self.bindPort))
        
        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.bind((self.host,self.bindPort))
        s2.connect((self.host,int(self.connectPort)))

        self.app.ui.writeMsg('Connected to :' + self.host +  " : " + str(self.connectPort) )
        
        self.socket = s2
        self.socket.send(self.app.crypto.public)

        start_new_thread(self.receive,(s2,))

    def sockets(self):
        s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        s1.bind((self.host,self.bindPort))
        self.app.ui.writeMsg("Listening on host :" + str(self.host) + " : " + str(self.bindPort))
        
        s1.listen(5)
        
        while True:
            c,addr = s1.accept()
            if self.isConnect:
                s1.close()
                break
            self.app.ui.writeMsg('Connected to :' + addr[0] +  " : " + str(addr[1]) )
            self.socket = c
            self.print_lock.acquire()
            start_new_thread(self.receive,(c,))

        if not self.isConnect:
            s1.close()

