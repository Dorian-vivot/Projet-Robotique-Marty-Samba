from martypy import Marty, MartyConnectException
from PyQt6.QtCore import QObject, pyqtSignal

class MartyConnection(QObject):

    connected = pyqtSignal()
    disconnected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._marty = None
        self._ip = ""
        self._is_connected = False

    def getIp(self) -> str:
        return self._ip
    
    def isConnected(self) -> bool:
        return self._is_connected
    
    def connect(self, ip : str) -> bool:
        if self._is_connected:
            self.disconnect()

        try:
            self._marty = Marty("wifi", ip)
            if self._marty.hello():
                self._ip = ip
                self._is_connected = True
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