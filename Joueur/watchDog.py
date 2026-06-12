from PyQt6.QtCore import QThread, pyqtSignal

"""
Classe qui utilise un Thread de la bibliothèque PyQt qui tourne en arrère-plan après la connexion du robot 

Toutes les 5 secondes, on demande le niveau de batterie du robot et de la couleur sous ses pieds
Si une requête n'aboutie pas lève une exception ou retourne None alors on informe l'interface de la déconnexion du robot

Cette classe peut émettre des signaux (alertes) :
    connection_lost : émis quand le robot ne répond plus
    battery_update(int) : niveau de batterie en pourcentage
    color_update(str) : couleur détectée au sol
"""
class WatchDog(QThread):
    
    connection_lost = pyqtSignal()
    battery_update = pyqtSignal(int)
    color_update = pyqtSignal(str)

    def __init__(self, connection):
        super().__init__()
        self._connection = connection
        self._is_running = False
    
    def run(self):
        self._is_running = True

        while self._is_running:
            if self._connection.getMarty() is not None and self._connection.isConnected():
                try:
                    battery_level = self._connection.getBatteryLevel()
                    if battery_level is not None:
                        self.battery_update.emit(battery_level)
                    else:
                        self.connection_lost.emit()

                    read_color = self._connection.getStandardFootColor()
                    if read_color is not None:
                        self.color_update.emit(read_color)
                except Exception as e:
                    self.connection_lost.emit()
                    self._is_running = False
                    print(f"Erreur avec la communication avec le robot : {e}")
            self.msleep(500)

    def stop(self):
        self._is_running = False
        self.wait()