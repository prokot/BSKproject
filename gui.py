import tkinter as tk

class GUI:
        
    def __init__(self) -> None:
        self.window = tk.Tk()
        label = tk.Label(text="BSK")
        label.pack()

        frame_log = tk.Frame()

        text_log = tk.Text(master = frame_log, background="black",foreground="white")
        text_log.insert("1.0","Sample text.")
        text_log.pack(fill=tk.BOTH,expand=True)

        frame_log.pack(fill=tk.BOTH,expand=True)

        frame_entry = tk.Frame()

        textField = tk.Entry(master=frame_entry)

        textField.pack(expand=True,fill=tk.BOTH,side=tk.LEFT)


        sendBttn = tk.Button(text="Send",master=frame_entry)
        sendBttn.pack(side=tk.LEFT,fill=tk.BOTH)
        frame_entry.pack(fill=tk.BOTH,expand=True)

    def mainLoop(self):
        self.window.mainloop()
