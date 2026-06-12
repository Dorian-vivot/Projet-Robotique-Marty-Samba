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

    loader = Dance_Loader()
    loader.load_path("example.dance")

    print("\n=== Chargement d'un fichier inexistant ===")
    try:
        loader.load_path("inexistant.dance")
    except FileNotFoundError as e:
        print(f"  FileNotFoundError : {e}")

    sys.exit()
    main()