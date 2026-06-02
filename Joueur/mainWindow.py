from PyQt6.QtWidgets import QMainWindow, QTabWidget
from controlWidget import ControlWidget
from danceWidget import DanceWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Marty - Joueur")
        self.setMinimumSize(1000, 800)
        self.tabs = QTabWidget()
        self.tabs.addTab(ControlWidget(), "Menu - Contrôle")
        self.tabs.addTab(DanceWidget(), "Menu - Dance")
        self.setCentralWidget(self.tabs)
       
