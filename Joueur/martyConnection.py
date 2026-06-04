from martypy import Marty, MartyConnectException
from PyQt6.QtCore import QObject, pyqtSignal

from watchDog import WatchDog

class MartyConnection(QObject):

    connected = pyqtSignal()
    disconnected = pyqtSignal()
    connection_lost = pyqtSignal()
    battery_update = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._marty = None
        self._ip = ""
        self._is_connected = False
        self._watchdog = None

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

    def getBatteryLevel(self) -> int | None:
        try:
            return int(self._marty.get_battery_remaining())
        except Exception:
            return None
        
    def _start_watchdog(self):
        self._watchdog = WatchDog(self)
        self._watchdog.connection_lost.connect(self._on_connection_lost)
        self._watchdog.battery_update.connect(self.battery_update)
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