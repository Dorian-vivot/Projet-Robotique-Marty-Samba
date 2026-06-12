import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                              QFileDialog)
from PyQt6.QtCore import QTimer

BASE = 'http://localhost:8000'


class RobotsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.refresh_btn.clicked.connect(self._rafraichir)
        self._timer = QTimer()
        self._timer.timeout.connect(self._rafraichir)
        self._timer.start(2000)
        self._rafraichir()

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

        # Chargement du fichier .battle
        battle_group = QGroupBox("Fichier Battle")
        battle_layout = QHBoxLayout()
        self.battle_label = QLabel("Aucun fichier chargé")
        self.battle_label.setStyleSheet("color: gray")
        self.battle_btn = QPushButton("Charger fichier .battle")
        self.battle_btn.clicked.connect(self._charger_battle)
        battle_layout.addWidget(self.battle_label)
        battle_layout.addWidget(self.battle_btn)
        battle_group.setLayout(battle_layout)

        layout.addWidget(statut_group)
        layout.addWidget(battle_group)
        layout.addWidget(robots_group)

    def _charger_battle(self):
        # Ouvre un explorateur de fichiers pour sélectionner un fichier .battle
        chemin, _ = QFileDialog.getOpenFileName(self, "Charger fichier .battle", "", "Fichiers Battle (*.battle)")
        if not chemin:
            return
        try:
            # Envoie le chemin au serveur qui charge les règles via BattleLoader
            r = requests.post(f'{BASE}/battle', json={'path': chemin}, timeout=2)
            if r.status_code == 200:
                nom_fichier = chemin.split('/')[-1]
                self.battle_label.setText(f"Chargé : {nom_fichier}")
                self.battle_label.setStyleSheet("color: green")
            else:
                self.battle_label.setText("Erreur : fichier invalide")
                self.battle_label.setStyleSheet("color: red")
        except Exception:
            self.battle_label.setText("Erreur : serveur inactif")
            self.battle_label.setStyleSheet("color: red")

    def _rafraichir(self):
        try:
            r = requests.get(f'{BASE}/robots', timeout=1)
            donnees = r.json()
            self.statut_label.setText("Actif")
            self.statut_label.setStyleSheet("color: green")
            self.tableau.setRowCount(len(donnees))
            for i, (robot_id, infos) in enumerate(donnees.items()):
                self.tableau.setItem(i, 0, QTableWidgetItem(robot_id))
                self.tableau.setItem(i, 1, QTableWidgetItem(str(infos['score'])))
                self.tableau.setItem(i, 2, QTableWidgetItem(str(infos['nombre_pas'])))
        except Exception:
            self.statut_label.setText("Inactif")
            self.statut_label.setStyleSheet("color: red")
            self.tableau.setRowCount(0)
