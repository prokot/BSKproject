from fileinput import filename
import tkinter as tk
from tkinter import filedialog
from os.path import expanduser

class GUI:
        
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.msgCnt = 0


        

    def writeMsg(self, msg):
        self.msgCnt += 1
        self.window.nametowidget("frame_log").nametowidget("text").insert(tk.END,"\n" + msg)

    def sendMsg(self,msg):
        self.writeMsg(msg)
        self.window.nametowidget("frame_entry").nametowidget("entry_field").delete(0,tk.END)

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
        label = tk.Label(text="BSK")
        label.pack()

        frame_log = tk.Frame(name ="frame_log")

        text_log = tk.Text(master = frame_log, background="black",foreground="white",name="text")
        text_log.insert(tk.END,"Sample text.")
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

        self.window.mainloop()


