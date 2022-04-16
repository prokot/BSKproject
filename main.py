import gui
import network as ntwrk
import sys
import crypto

class App:
    def __init__(self) -> None:
        self.port = sys.argv[1]
        self.crypto = crypto.Crpto(self)
        self.ui = gui.GUI(self)
        self.ntwrk = ntwrk.P2P(self,self.port)
        self.ui.mainLoop()

if __name__ == "__main__":
    app = App()