import socket
from _thread import *
import threading as thrd
import gui

class P2P:
    def __init__(self) -> None:
        self.print_lock = thrd.Lock()


    def send(self,c,msg):
        while True:
            data = c.send(msg)

    def receive(self,c):

        

    def sockets(self):
        host = "127.0.0.1"

        portS = 180400
        portR = 180401

        s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s1.bind((host,portS))
        
        s1.listen(5)

        while True:
            c,addr = s1.accept()

            self.print_lock.acquire()
            print('Connected to :', addr[0], " : ", addr[1] )

            start_new_thread(self.send,(c,))
        s.close()

