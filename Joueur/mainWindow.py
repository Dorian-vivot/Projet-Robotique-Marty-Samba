from PyQt6.QtWidgets import QMainWindow, QTabWidget
from controlWidget import ControlWidget
from danceWidget import DanceWidget
from martyConnection import MartyConnection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Une seule instance MartyConnection partagée entre les deux widgets
        self._connection = MartyConnection()
        self.setWindowTitle("Marty - Joueur")
        self.setMinimumSize(1000, 800)
        self.tabs = QTabWidget()
        self.tabs.addTab(ControlWidget(self._connection), "Menu - Contrôle")
        self.tabs.addTab(DanceWidget(self._connection), "Menu - Dance")
        self.setCentralWidget(self.tabs)
       
