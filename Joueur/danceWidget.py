from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QLabel, QLineEdit, QPushButton, QFileDialog)

from arbitreClient import ArbitreClient
from martyConnection import MartyConnection
from Dance_Loader import Dance_Loader


class DanceWidget(QWidget):
    def __init__(self, connection: MartyConnection):
        super().__init__()
        self._connection = connection
        self._connection.disconnected.connect(self._on_marty_deconnecte)
        self._connection.connection_lost.connect(self._on_marty_deconnecte)
        self._arbitre = ArbitreClient()
        self._dance_loader = Dance_Loader()
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

        # Bouton connexion
        self.connect_btn = QPushButton("Se connecter à l'arbitre")
        self.connect_btn.clicked.connect(self._connecter)
        connexion_layout.addWidget(self.connect_btn)

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

        # Groupe chorégraphie
        chore_group = QGroupBox("Chorégraphie")
        chore_layout = QVBoxLayout()

        # Bouton charger .dance
        dance_layout = QHBoxLayout()
        self.dance_label = QLabel("Aucun fichier chargé")
        self.dance_label.setStyleSheet("color: gray")
        self.load_dance_btn = QPushButton("Charger fichier .dance")
        self.load_dance_btn.clicked.connect(self._charger_dance)
        dance_layout.addWidget(self.dance_label)
        dance_layout.addWidget(self.load_dance_btn)
        chore_layout.addLayout(dance_layout)

        self.start_btn = QPushButton("Démarrer la chorégraphie")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self._demarrer)
        chore_layout.addWidget(self.start_btn)

        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("Score :"))
        self.score_label = QLabel("—")
        score_layout.addWidget(self.score_label)
        score_layout.addStretch()
        chore_layout.addLayout(score_layout)

        chore_group.setLayout(chore_layout)
        layout.addWidget(chore_group)
        layout.addStretch()

    def _on_marty_deconnecte(self):
        # Si Marty se déconnecte, on prévient l'arbitre automatiquement
        if self._arbitre.is_connected():
            self._deconnecter()

    def _charger_dance(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Charger fichier .dance", "", "Fichiers Dance (*.dance)")
        if not chemin:
            return
        try:
            self._dance_loader.load_path(chemin)
            nom = chemin.split('/')[-1]
            self.dance_label.setText(f"Chargé : {nom}")
            self.dance_label.setStyleSheet("color: green")
        except Exception:
            self.dance_label.setText("Erreur : fichier invalide")
            self.dance_label.setStyleSheet("color: red")

    def _connecter(self):
        ip = self.input_ip.text().strip() or 'localhost'
        self._arbitre = ArbitreClient(host=ip)
        try:
            rid = self._arbitre.hello()
            self.statut_label.setText(f"Connecté — RID : {rid}")
            self.statut_label.setStyleSheet("color: green")
            self.connect_btn.setText("Se déconnecter")
            self.connect_btn.clicked.disconnect()
            self.connect_btn.clicked.connect(self._deconnecter)
            self.start_btn.setEnabled(True)
        except Exception:
            self.statut_label.setText("Erreur : arbitre inaccessible")
            self.statut_label.setStyleSheet("color: red")

    def _deconnecter(self):
        self._arbitre.bye()
        self.statut_label.setText("Non connecté")
        self.statut_label.setStyleSheet("color: gray")
        self.connect_btn.setText("Se connecter à l'arbitre")
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self._connecter)
        self.start_btn.setEnabled(False)
        self.score_label.setText("—")

    def _demarrer(self):
        try:
            nb_mouvements = self._arbitre.start()
            self.score_label.setText(f"0  ({nb_mouvements} mouvements)")
        except Exception:
            self.statut_label.setText("Erreur : arbitre inaccessible")
            self.statut_label.setStyleSheet("color: red")
