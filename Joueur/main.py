import sys
from PyQt6.QtWidgets import QApplication, QWidget
from mainWindow import MainWindow
from Dance_Loader import Dance_Loader

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()