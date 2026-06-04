import sys
import threading
from PyQt6.QtWidgets import QApplication
from Battle_Loader import BattleLoader
from mainWindow import MainWindow
import serveur


def lancer_serveur():
    serveur.app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    loader = BattleLoader()

    flask_thread = threading.Thread(target=lancer_serveur, daemon=True)
    flask_thread.start()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
