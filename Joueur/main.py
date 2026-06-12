import sys
from PyQt6.QtWidgets import QApplication, QWidget
from mainWindow import MainWindow
import Dance_Loader

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    print(f"Directions valides : {Dance_Loader.Valid_Directions}")
    print(f"Bras valides : {Dance_Loader.Valid_Arms}")
    print(f"Dexpressions valides : {Dance_Loader.Valid_Expressions}")
    for direction in Dance_Loader.Valid_Directions:
        step = Dance_Loader.DanceStep(1, direction)
        print(f"{step}")
    
    try:
        bad = Dance_Loader.DanceStep(1, "zozo")
    except ValueError as e:
        print(f"Erreur capturée : {e}")
    sys.exit()
    main()