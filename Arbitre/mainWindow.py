from PyQt6.QtWidgets import QMainWindow, QTabWidget
from robotsWidget import RobotsWidget
from activiteWidget import ActiviteWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arbitre - Dance Battle")
        self.setMinimumSize(800, 600)

        tabs = QTabWidget()
        tabs.addTab(RobotsWidget(), "Robots connectés")
        tabs.addTab(ActiviteWidget(), "Activité")
        self.setCentralWidget(tabs)
