import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QLabel, QTableWidget, QTableWidgetItem, QPushButton)

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

        # Tableau des robots
        robots_group = QGroupBox("Robots connectés")
        robots_layout = QVBoxLayout()

        self.tableau = QTableWidget(0, 3)
        self.tableau.setHorizontalHeaderLabels(["Robot ID", "Score", "Pas effectués"])
        self.tableau.horizontalHeader().setStretchLastSection(True)
        self.tableau.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        robots_layout.addWidget(self.tableau)

        self.refresh_btn = QPushButton("Rafraîchir")
        robots_layout.addWidget(self.refresh_btn)

        robots_group.setLayout(robots_layout)

        layout.addWidget(statut_group)
        layout.addWidget(robots_group)
