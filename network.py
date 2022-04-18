from select import select
import socket
from _thread import *
import threading as thrd
from time import sleep
import gui
from main import App
from Crypto.Cipher import AES
import pickle as plk
import os

class P2P:
    
    maxPacketSize = 2048
    sendProgress = 0

    def __init__(self,app,bindPort) -> None:
        self.print_lock = thrd.Lock()
        self.isConnect = False
        self.connectPort = 0
        self.app = app
        self.host = "127.0.0.1"
        self.bindPort = int(bindPort)
        self.pubKey = 0
        start_new_thread(self.sockets)

    def sendFile(self,path):
        with open(path,'rb') as file:
            data = file.read()
            file.close()
        ext = os.path.splitext(path)
        filename = ext[0].split('/')[-1]
        ext = ext[1]
        data = self.app.crypto.encryptDataCBC(data,self.app.crypto.session)
        data["ext"] = ext
        data["filename"] = filename
        data = plk.dumps(data)
        leng = len(data) + 10
        self.socket.send(leng.to_bytes(4,'little'))
        #self.socket.send(data)
        global cnt 
        cnt = 0
        prg = leng/self.maxPacketSize

        

        if leng > 500000000:
            start_new_thread(self.calculateProgressXD,(prg,))

            for x in range(0,leng,self.maxPacketSize):

                self.socket.send(data[x:x+(self.maxPacketSize)])        #FIX LONG DATA TRANSFER WITH LOADING BAR, MAYBE ADD TKINTER PROGRESS BAR IDK
                cnt+=1
        else: 
            self.socket.send(data)
        self.sendProgress = 0
        sleep(0.00000002)

    def calculateProgressXD(self,prg):          # XD
        while self.sendProgress < 11:
            self.sendProgress = int((cnt*100)/prg)


    def send(self,msg):
        #data = self.app.crypto.decryptData(self.app.crypto.encryptData(msg.encode('ascii')))
        data = self.app.crypto.encryptDataCBC(msg.encode('ascii'),self.app.crypto.session)
        data["ext"] = "string"
        data = plk.dumps(data)
        leng = len(data)
        self.socket.send(leng.to_bytes(4,'little'))
        self.socket.send(data)

    def receive(self,c):

        while True:
            dataLen = c.recv(4)
            dataLen = int.from_bytes(dataLen,"little")
            data = []
            for x in range(int(dataLen/self.maxPacketSize)+1):
            #while True:
                r, _, _ = select([c], [], [])
                if not r:
                    break
                packet = c.recv(self.maxPacketSize)
                data.append(packet)
                #sleep(0.1)

            # data = c.recv(dataLen)
            # leng = len(data)
            data = b"".join(data)
            data = plk.loads(data)
            ext = data["ext"]
            if not ext == "string":
                filename = data["filename"]

            data = self.app.crypto.decryptDataCBC(data,self.app.crypto.session)

            if(ext == "string"): 
                self.app.ui.writeMsg(str(self.connectPort) + ">" + data.decode('ascii'))
            else:
                # with open(os.getcwd()+ filename+ext,'w+') as file:
                #     file.close()
                with open(str(self.bindPort)+ "/" + filename+ext,'wb+') as file:
                    try:
                        file.write(data)
                    except Exception as ex:
                        pass
                    finally:
                        file.close()
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
        self.socket.send(self.app.crypto.public.exportKey())
        data = self.socket.recv(256)
        self.app.crypto.session = self.app.crypto.decryptDataRSA(data,self.app.crypto.private)
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
            self.connectPort = str(addr[1])
            self.socket = c
            pubkey = self.socket.recv(1024)
            sendData = self.app.crypto.encryptDataRSA(self.app.crypto.generateSesKey(),pubkey)
            self.socket.send(sendData)
            
            self.print_lock.acquire()
            start_new_thread(self.receive,(c,))

        if not self.isConnect:
            s1.close()

