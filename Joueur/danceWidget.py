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
