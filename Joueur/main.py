import sys
from PyQt6.QtWidgets import QApplication, QWidget
from mainWindow import MainWindow
from Dance_Loader import DanceStep

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    step1 = DanceStep(2, "B")
    step2 = DanceStep(1, "U")
    step3 = DanceStep(1, "L")

    print("=== Test DanceStep ===")
    print(step1)
    print(step2)
    print(step3)
    print(f"step2.nb_pas    = {step2.nb_pas}")
    print(f"step1.direction = {step1.direction}")
    sys.exit()
    main()