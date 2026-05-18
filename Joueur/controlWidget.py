from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout, QWidget

class ControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)

        # Groupe Box état du robot
        state_group = QGroupBox("État du robot")
        state_group.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Maximum)
        state_hbox = QHBoxLayout()

        # Groupe Box de connexion
        connexion_group = QGroupBox("Connexion au Robot")
        connexion_group.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Maximum)
        connexion_hbox = QHBoxLayout()

        # ------ Groupe - Connexion (Gauche) : Saisie manuelle ------
        left_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        left_layout.addLayout(input_layout)

        # Création du label
        label_input_ip = QLabel("Saisir IP : ")
        input_layout.addWidget(label_input_ip)

        # Création de l'input
        input_ip = QLineEdit()
        input_ip.setPlaceholderText("Adresse IP de Marty (ex : 192.168.1.12)")
        input_layout.addWidget(input_ip)

        # Création du boutton de connexion
        connexion_button = QPushButton("Se connecter")
        left_layout.addWidget(connexion_button)
        left_layout.addStretch()

        # ------ Groupe - Connexion (Droite) : Recherche automatique ------
        right_layout = QVBoxLayout()

        # Liste déroulante des robots
        self.marty_list = QListWidget()
        self.marty_list.setMaximumHeight(60)
        test_ROBOT = QListWidgetItem("Marty - 192.168.1.1")
        test_ROBOT.setData(Qt.ItemDataRole.UserRole,"192.168.1.1")
        self.marty_list.addItem(test_ROBOT)
        right_layout.addWidget(self.marty_list)

        # Création du boutton de recherche automatique
        scan_button = QPushButton("Lancer le scan") # TODO : Pour lancer le scan utiliser QThread pour ne pas figer l'UI car la recherche prend du temps puis actualiser la liste des robots
        right_layout.addWidget(scan_button)

        # Création du boutton de recherche automatique
        connexion_button_auto = QPushButton("Connecter")
        right_layout.addWidget(connexion_button_auto)
        right_layout.addStretch()
        
        connexion_hbox.addLayout(left_layout)
        connexion_hbox.addLayout(right_layout)
        connexion_group.setLayout(connexion_hbox)
        
        other_group = QGroupBox("Autres")

        # Ajout des GroupBox
        self.main_layout.addWidget(state_group)
        self.main_layout.addWidget(connexion_group)
        self.main_layout.addWidget(other_group)
        self.main_layout.addStretch()
        

