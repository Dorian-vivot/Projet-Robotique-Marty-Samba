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

    seq_lines = [
    "SEQ 1",
    "1U",
    "1L",
    "2B",
    "2R",
    "1U",
    "1L",
    "",           # ligne vide intentionnelle
    "MAUVAISE",   # ligne invalide
    ]

    print("=== Parsing section SEQ ===")
    steps = Dance_Loader().parse_sequence(seq_lines)
    print(f"\n{len(steps)} mouvements parsés :")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    sys.exit()
    main()