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
    loader=Dance_Loader()
    loader.load_path("example.dance")

    print("\n=== Mouvements chargés ===")
    for i, step in enumerate(loader.steps, 1):
        print(f"  {i}. {step}")

    print("\n=== Règles ACT chargées ===")
    for color, action in loader.action_by_color.items():
        print(f"  {action}")

    print("\n=== Lookup couleur ===")
    for couleur in ["N", "B", "R", "V"]:
        result = loader.get_action_for_color(couleur)
        print(f"  Couleur {couleur!r} → {result}")

    print("\n=== Chargement d'un fichier inexistant ===")
    try:
        loader.load_path("inexistant.dance")
    except FileNotFoundError as e:
        print(f"  FileNotFoundError : {e}")
    sys.exit()
    main()