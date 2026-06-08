from martypy import Marty, MartyConnectException
from PyQt6.QtCore import QObject, pyqtSignal

from colorAlgorithm import ColorAlgorithm
from watchDog import WatchDog

"""
Classe qui gére la connexion du robot et exécute les réquêtes vers le robot

Cette classe peut émettre des signaux (alertes) :
    connected : émis quand la connexion est établie avec succès
    disconnected : émis lors d'une déconnexion volontaire
    connection_lost : émis quand le WatchDog détecte une perte de connexion
    battery_update(int) : relayé depuis WatchDog
    color_update(str) : relayé depuis WatchDog
"""
class MartyConnection(QObject):

    connected = pyqtSignal()
    disconnected = pyqtSignal()
    connection_lost = pyqtSignal()
    battery_update = pyqtSignal(int)
    color_update = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._marty = None
        self._ip = ""
        self._is_connected = False
        self._watchdog = None
        self._colorAlgorithm = ColorAlgorithm()

    def getIp(self) -> str:
        return self._ip
    
    def isConnected(self) -> bool:
        return self._is_connected
    
    def getMarty(self) -> Marty:
        return self._marty
    
    def connect(self, ip : str) -> bool:
        if self._is_connected:
            self.disconnect()

        try:
            self._marty = Marty("wifi", ip)
            if self._marty.hello():
                self._ip = ip
                self._is_connected = True
                self._start_watchdog()
                self.connected.emit()
                return True
            else:
                self._marty.close()
                self._marty = None
                self._is_connected = False
                return False
        except MartyConnectException as e:
            print(f"Erreur lors de la connexion à {ip} : {e}")
            return False
        except Exception as e:
            print(f"Erreur : {e}")
            return False
    
    def disconnect(self):
        self._stop_watchdog()
        if self._marty is not None and self._is_connected:
            try:
                self._marty.close()
            except Exception as e:
                print(f"Erreur lors de la déconnexion : {e}")
            finally:
                self._marty = None

        self._ip = ""
        self._is_connected = False
        self.disconnected.emit() 

    def getStandardFootColor(self, colorSensorSide = "left") -> str:
        if self._marty is not None and self._is_connected:
            try:
                hex_color = self._marty.get_color_sensor_hex(colorSensorSide)
                print(hex_color)
                return self._colorAlgorithm.get_color_hex_to_standard(hex_color)
            except Exception as e:
                print(f"Erreur pour récupérer la couleur aux pieds : {e}")
                return None

    def getBatteryLevel(self) -> int | None:
        try:
            return int(self._marty.get_battery_remaining())
        except Exception:
            print(f"Erreur pour récupérer le niveau de batterie")
            return None
        
    def _start_watchdog(self):
        self._watchdog = WatchDog(self)
        self._watchdog.connection_lost.connect(self._on_connection_lost)
        self._watchdog.battery_update.connect(self.battery_update)
        self._watchdog.color_update.connect(self.color_update)
        self._watchdog.start()

    def _stop_watchdog(self):
        if self._watchdog is not None:
            self._watchdog.stop()
            self._watchdog = None

    def _on_connection_lost(self):
        self._marty = None
        self._ip = ""
        self._watchdog = None 
        self._is_connected = False
        self.connection_lost.emit()