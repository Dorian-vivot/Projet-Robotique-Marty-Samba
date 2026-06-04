from PyQt6.QtCore import QThread, pyqtSignal

class WatchDog(QThread):
    
    connection_lost = pyqtSignal()
    battery_update = pyqtSignal(int)

    def __init__(self, connection):
        super().__init__()
        self._connection = connection
        self._is_running = False
    
    def run(self):
        self._is_running = True

        while self._is_running:
            if self._connection.getMarty() is not None and self._connection.isConnected():
                try:
                    self._connection.getMarty().hello()
                    battery_level = self._connection.getBatteryLevel()
                    if battery_level is not None:
                        self.battery_update.emit(battery_level)
                except Exception:
                    self.connection_lost.emit()
                    self._is_running = False
                    return 
            self.sleep(5)

    def stop(self):
        self._is_running = False
        self.wait()