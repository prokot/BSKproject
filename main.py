import gui
import network as ntwrk
import sys

class App:
    def __init__(self) -> None:
        self.ui = gui.GUI(self)
        self.ntwrk = ntwrk.P2P(self,sys.argv[1])
        self.ui.mainLoop()

if __name__ == "__main__":
    app = App()