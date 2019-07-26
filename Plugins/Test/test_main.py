from PyQt5.QtWidgets import *

WIN_TITLE = 'Test'
WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT = [20, 80, 200, 150]

class Window(QMainWindow):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.setWindowTitle(WIN_TITLE)
        self.setGeometry(WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT)
