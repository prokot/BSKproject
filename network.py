from select import select
import socket
from _thread import *
import threading as thrd
from time import sleep
import gui
from main import App
from Crypto.Cipher import AES
import pickle as pkl
import os


#TODO:
# -Very slow transfer of sliced files, with progress bar added. 
# I used a lot of threads to do that and it's still very slow
# -Add connection closing when exiting the app.

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
        self.cipher = "CBC"
        start_new_thread(self.sockets)

    def encrypt(self,data):
        if self.cipher == "CBC":
            return self.app.crypto.encryptDataCBC(data,self.app.crypto.session)
        else:
            return self.app.crypto.encryptDataECB(data,self.app.crypto.session)

    def decrypt(self,data):
        if self.cipher == "CBC":
            return self.app.crypto.decryptDataCBC(data,self.app.crypto.session)
        else:
            return self.app.crypto.decryptDataECB(data,self.app.crypto.session)

    def sendFile(self,path):
        with open(path,'rb') as file:
            data = file.read()
            file.close()
        ext = os.path.splitext(path)
        filename = ext[0].split('/')[-1]
        ext = ext[1]
        data = self.encrypt(data)
        data["ext"] = ext
        data["filename"] = filename
        data["cipher"] = self.cipher
        data = pkl.dumps(data)
        leng = len(data) + 10
        self.socket.send(leng.to_bytes(4,'little'))
        global cnt 
        cnt = 0
        prg = leng/self.maxPacketSize

        if leng > 500000000:
            start_new_thread(self.calculateProgressXD,(prg,))
            for x in range(0,leng,self.maxPacketSize):
                self.socket.send(data[x:x+(self.maxPacketSize)])
                cnt+=1
        else: 
            self.socket.send(data)
        self.sendProgress = 0

    def calculateProgressXD(self,prg):          # XD
        while self.sendProgress < 11:
            self.sendProgress = int((cnt*100)/prg)


    def send(self,msg):
        data = self.encrypt(msg.encode('ascii'))
        data["ext"] = "string"
        data["cipher"] = self.cipher
        data = pkl.dumps(data)
        leng = len(data)
        self.socket.send(leng.to_bytes(4,'little'))
        self.socket.send(data)

    def closeConnection(self):
        try:
            data = self.encrypt("".encode('ascii'))
            data["ext"] = "close"
            data["cipher"] = self.cipher
            data = pkl.dumps(data)
            leng = len(data)
            self.socket.send(leng.to_bytes(4,'little'))
            self.socket.send(data)
        except:
            pass

    def receive(self,c):

        while True:
            dataLen = c.recv(4)
            if not dataLen:
                break
            dataLen = int.from_bytes(dataLen,"little")
            data = []
            for x in range(int(dataLen/self.maxPacketSize)+1):
                r, _, _ = select([c], [], [])
                if not r:
                    break
                packet = c.recv(self.maxPacketSize)
                data.append(packet)
            if (data==b""):
                break
            data = b"".join(data)
            data = pkl.loads(data)

            ext = data["ext"]
            
            if "filename" in data.keys():
                filename = data["filename"]

            if data["cipher"] == "CBC":
                data = self.app.crypto.decryptDataCBC(data,self.app.crypto.session)
            else:
                data = self.app.crypto.decryptDataECB(data,self.app.crypto.session)

            if(ext == "string"): 
                self.app.ui.writeMsg(str(self.connectPort) + ">" + data.decode('ascii'))
            elif (ext =="ack"):
                continue
            elif (ext == "close"):
                break
            else:
                with open(str(self.bindPort)+ "/" + filename+ext,'wb+') as file:
                    try:
                        file.write(data)
                    except Exception as ex:
                        pass
                    finally:
                        file.close()
            if not (ext == "ack"):
                data = self.encrypt("".encode('ascii'))
                data["ext"] = "ack"
                data["cipher"] = self.cipher
                data = pkl.dumps(data)
                leng = len(data)
                self.socket.send(leng.to_bytes(4,'little'))
                self.socket.send(data)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def connect(self,port):
        self.connectPort = port
        self.isConnect = True
        
        socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM).connect( (self.host, self.bindPort))
        
        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s2.bind((self.host,self.bindPort))
        s2.connect((self.host,int(self.connectPort)))
        self.app.ui.writeMsg('Connected to :' + self.host +  " : " + str(self.connectPort) )
        
        self.socket = s2
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.send(self.app.crypto.public.exportKey())
        data = self.socket.recv(256)
        self.app.crypto.session = self.app.crypto.decryptDataRSA(data,self.app.crypto.private)
        start_new_thread(self.receive,(s2,))

    def sockets(self):
        s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.bind((self.host,self.bindPort))
        self.app.ui.writeMsg("Listening on host :" + str(self.host) + " : " + str(self.bindPort))
        
        s1.listen(5)
        
        while True:
            c,addr = s1.accept()
            if self.isConnect:
                c.shutdown(socket.SHUT_RDWR)
                s1.close()
                break
            self.app.ui.writeMsg('Connected to :' + addr[0] +  " : " + str(addr[1]) )
            self.connectPort = str(addr[1])
            self.socket = c
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            pubkey = self.socket.recv(1024)
            sendData = self.app.crypto.encryptDataRSA(self.app.crypto.generateSesKey(),pubkey)
            self.socket.send(sendData)
            
            self.print_lock.acquire()
            start_new_thread(self.receive,(c,))