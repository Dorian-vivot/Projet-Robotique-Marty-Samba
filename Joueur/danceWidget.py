from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QLabel, QLineEdit, QPushButton)

from arbitreClient import ArbitreClient


class DanceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._arbitre = ArbitreClient()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Groupe connexion à l'arbitre
        connexion_group = QGroupBox("Connexion à l'arbitre")
        connexion_layout = QVBoxLayout()

        # Champ IP
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("IP Arbitre :"))
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("ex : 192.168.1.10  (vide = localhost)")
        ip_layout.addWidget(self.input_ip)
        connexion_layout.addLayout(ip_layout)

        # Statut
        statut_layout = QHBoxLayout()
        statut_layout.addWidget(QLabel("Statut :"))
        self.statut_label = QLabel("Non connecté")
        self.statut_label.setStyleSheet("color: gray")
        statut_layout.addWidget(self.statut_label)
        statut_layout.addStretch()
        connexion_layout.addLayout(statut_layout)

        connexion_group.setLayout(connexion_layout)
        layout.addWidget(connexion_group)
        layout.addStretch()
