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
    nb_definis = len(loader.steps)
    print(f"\nSéquence de base : {nb_definis} mouvements")

    print(f"\nsequence exacte")
    seq = loader.get_sequence(nb_definis)
    for i, s in enumerate(seq, 1):
        print(f"  {i}. {s}")

    print(f"\nsequence vide")
    seq = loader.get_sequence(0)
    print(f"  Résultat : {seq}")
    sys.exit()
    main()