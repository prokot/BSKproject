from fileinput import filename
import tkinter as tk
from tkinter import DISABLED, filedialog
from os.path import expanduser
from tkinter.font import NORMAL
import network as ntwrk
from _thread import *
import threading as thrd
from main import App

class GUI:
        
    def __init__(self,app) -> None:
        self.window = tk.Tk()
        self.msgCnt = 0
        self.app = app

        label = tk.Label(text="BSK")
        label.pack()
        connect_frame = tk.Frame()
        port_entry = tk.Entry(master=connect_frame)
        port_entry.pack(side=tk.LEFT)

        connect_bttn = tk.Button(text = "Connect",master=connect_frame,command = lambda : self.app.ntwrk.connect(port_entry.get())).pack(side=tk.LEFT)
        connect_frame.pack()
        frame_log = tk.Frame(name ="frame_log")

        text_log = tk.Text(master = frame_log, background="black",foreground="white",name="text")
        text_log.insert(tk.END,"Sample text.")
        text_log.config(state=DISABLED)
        text_log.pack(fill=tk.BOTH,expand=True)

        frame_log.pack(fill=tk.BOTH,expand=True)

        frame_entry = tk.Frame(name = "frame_entry")

        textField = tk.Entry(master=frame_entry,name="entry_field")

        textField.pack(expand=True,fill=tk.BOTH,side=tk.LEFT)

        frame_bttns = tk.Frame()

        sendBttn = tk.Button(text="Send",master=frame_bttns,command = lambda: self.sendMsg(textField.get())).pack(fill=tk.BOTH)
        fileBttn = tk.Button(text="Choose file",master=frame_bttns, command = self.fileBrowser).pack(fill=tk.BOTH)

        frame_entry.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)
        frame_bttns.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        
        self.window.bind("<Key>", self.keyPressHandler)
        pswrd_wind = tk.Tk()
        pswrd_wind.geometry("+"+str(self.window.winfo_x() + int(self.window.winfo_width()/2)) +"+" + str(self.window.winfo_y() + int(self.window.winfo_height()/2)))
        pswrd_label = tk.Label(pswrd_wind,text="Enter password:").pack()
        pswrd_entry = tk.Entry(pswrd_wind)
        pswrd_entry.pack()
        pswrd_bttn = tk.Button(pswrd_wind,text="Ok",command = lambda: self.pwdDestroy(pswrd_wind,pswrd_entry.get())).pack()
        self.pwd_window = pswrd_wind
        

    def pwdDestroy(self,window,pwd):
        window.destroy()
        self.app.crypto.generateLocalKey(pwd)


    def writeMsg(self, msg):
        self.msgCnt += 1
        self.window.nametowidget("frame_log").nametowidget("text").config(state=NORMAL)
        self.window.nametowidget("frame_log").nametowidget("text").insert(tk.END,"\n" + msg)
        self.window.nametowidget("frame_log").nametowidget("text").config(state=DISABLED)

    def sendMsg(self,msg):
        self.writeMsg(msg)
        self.window.nametowidget("frame_entry").nametowidget("entry_field").delete(0,tk.END)
        self.app.ntwrk.send(msg)

    def keyPressHandler(self,event):
        if event.char == '\r':
            self.sendMsg(self.window.nametowidget("frame_entry").nametowidget("entry_field").get())


    def fileBrowser(self):
        home = expanduser("~")
        fileName = filedialog.askopenfilename(initialdir=home,title="Select a file", filetypes = (("Text Files","*.txt"),
            ("Png files","*.png"),
            ("Pdf files","*.pdf"),
            ("Avi files","*.avi")))
        self.writeMsg("Wybrano plik: " + fileName)
        #return fileName

    def mainLoop(self):
        self.window.mainloop()
        self.pwd_window.mainloop()


