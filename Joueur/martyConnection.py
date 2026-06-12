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
                return self._colorAlgorithm.get_color_hex_to_standard(hex_color)
            except Exception as e:
                print(f"Erreur pour récupérer la couleur aux pieds : {e}")
                return None

    def getBatteryLevel(self) -> int | None:
        try:
            return int(self._marty.get_battery_remaining())
        except Exception as e:
            print(f"Erreur pour récupérer le niveau de batterie : {e}")
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

    def move(self, direction: str):
        try:
            if self._marty is not None and self._is_connected:
                step_length = 0
                if direction == "backward":
                    step_length = -40
                elif direction == "forward":
                    step_length = 40
                self._marty.walk(num_steps=1, start_foot="auto", turn=0, step_length=step_length, move_time=1500)
        except Exception as e:
            print(f"Erreur lors de l'éxécution du movement (Direction : {direction}) : {e}")

    def sidestep(self, side: str):
        try:
            if self._marty is not None and self._is_connected:
                self._marty.sidestep(side=side, steps=1, step_length=40, move_time=1500)
        except Exception as e:
            print(f"Erreur lors de l'éxécution du pas sur le coté (Coté : {side}) : {e}")
        

    def turn(self, direction: str):
        try:
            if self._marty is not None and self._is_connected:
                turn_val = 0
                if direction == "right":
                    turn_val = 180
                elif direction == "left":
                    turn_val = -180
                self._marty.walk(num_steps=1, start_foot="auto", turn=turn_val, step_length=0, move_time=5000)
        except Exception as e:
            print(f"Erreur lors de l'éxécution du demi-tour (Direction : {direction}) : {e}")

    def stop(self):
        try:
            if self._marty is not None and self._is_connected:
                self._marty.stop()
        except Exception as e:
            print(f"Erreur pour stopper l'éxécution : {e}")

    def moveArm(self, side: str, movement: str):
        try:
            if self._marty is not None and self._is_connected:
                joint = ""
                if side == "left":
                    joint = "left arm"
                elif side == "right":
                    joint = "right arm"

                angle = self._marty.get_joint_position(joint_name_or_num=joint)
                if movement == "raise":
                    angle += 45
                elif movement == "back":
                    angle -= 45
                self._marty.move_joint(joint_name_or_num=joint, position=angle, move_time=500)
        except Exception as e:
            print(f"Erreur pour bouger le bras (Direction : {side}, Mouvement : {movement}) : {e}")

    def armsNeutral(self):
        try:
            if self._marty is not None and  self._is_connected:
                self._marty.move_joint(joint_name_or_num="left arm",  position=0, move_time=500)
                self._marty.move_joint(joint_name_or_num="right arm", position=0, move_time=500)
        except Exception as e:
            print(f"Erreur pour bouger les bras à la position initial : {e}")
        
    def setEyesPose(self, pose: str):
        try:
            if self._marty is not None and self._is_connected:
                self._marty.eyes(pose_or_angle=pose, move_time=300)
        except Exception as e:
            print(f"Erreur lors de l'éxécution de la commmande eyes (Pose : {pose}) : {e}")

    def setExpression(self, pose: str, color: tuple):
        try:
            if self._marty is not None and self._is_connected:
                self._marty.eyes(pose_or_angle=pose, move_time=300)
                self._marty.disco_color(color, api='led')
        except Exception as e:
            print(f"Erreur lors de l'éxécution de l'expression (Pose : {pose}, Couleur : {color}) : {e}")