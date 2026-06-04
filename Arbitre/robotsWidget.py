import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QGroupBox, QLabel)

BASE = 'http://localhost:8000'


class RobotsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # État du serveur
        statut_group = QGroupBox("État du serveur")
        statut_layout = QHBoxLayout()
        self.statut_label = QLabel("Inactif")
        self.statut_label.setStyleSheet("color: red")
        statut_layout.addWidget(QLabel("Serveur :"))
        statut_layout.addWidget(self.statut_label)
        statut_layout.addStretch()
        statut_group.setLayout(statut_layout)

        layout.addWidget(statut_group)
        layout.addStretch()
