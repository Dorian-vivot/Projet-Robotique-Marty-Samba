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

    lignes_valides = ["1U", "1L", "2B", "2R", "10U", "3D"]
    lignes_invalides = ["", "ZZ", "U1", "1Z", "abc"]

    print("=== Lignes valides ===")
    for ligne in lignes_valides:
        step = Dance_Loader.parse_step_line(ligne)
        print(f"  {ligne!r} → {step}")

    print("\n=== Lignes invalides ===")
    for ligne in lignes_invalides:
        step = Dance_Loader.parse_step_line(ligne)
        print(f"  {ligne!r} → {step}")

    sys.exit()
    main()