import time

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QLabel, QLineEdit, QPushButton, QFileDialog)
from PyQt6.QtCore import QThread, pyqtSignal

from arbitreClient import ArbitreClient
from martyConnection import MartyConnection
from Dance_Loader import Dance_Loader


class _DanceThread(QThread):
    """Exécute la chorégraphie dans un thread séparé pour ne pas bloquer l'UI."""
    score_update = pyqtSignal(int)

    def __init__(self, connection, arbitre, dance_loader, nb_mouvements):
        super().__init__()
        self._connection = connection
        self._arbitre = arbitre
        self._loader = dance_loader
        self._nb = nb_mouvements

    def run(self):
        sequence = self._loader.get_sequence(self._nb)
        for step in sequence:
            self._marcher(step)
            time.sleep(1.8)  # attend que Marty finisse le mouvement
            couleur_standard = self._connection.getStandardFootColor() or ''
            lettre = self._map_couleur(couleur_standard)
            action = self._loader.get_action_for_color(lettre)
            arm = action.get_arms_string() if action else ''
            exp = action.expression if action else ''
            if action:
                self._executer_expression(arm, exp)
            self._arbitre.step(lettre, arm, exp)
            score = self._arbitre.score()
            self.score_update.emit(score)

    def _marcher(self, step):
        # Convertit la direction du .dance en commande Marty
        for _ in range(step.nb_pas):
            if step.direction == 'U':
                self._connection.move('forward')
            elif step.direction in ('D', 'B'):
                self._connection.move('backward')
            elif step.direction == 'L':
                self._connection.sidestep('left')
            elif step.direction == 'R':
                self._connection.sidestep('right')

    def _executer_expression(self, arms_str, exp):
        # Exécute les bras et l'expression sur Marty
        arm_map = {
            'ALU': ('left',  'raise'),
            'ALB': ('left',  'back'),
            'ARU': ('right', 'raise'),
            'ARB': ('right', 'back'),
        }
        for arm_code in arms_str.split('+'):
            if arm_code in arm_map:
                side, movement = arm_map[arm_code]
                self._connection.moveArm(side, movement)
        exp_map = {
            'XNT': ('normal',  (128, 128, 128)),
            'XSD': ('normal',  (0,   0,   255)),
            'XNG': ('angry',   (255, 0,   0  )),
            'XHP': ('excited', (0,   255, 0  )),
        }
        if exp in exp_map:
            pose, color = exp_map[exp]
            self._connection.setExpression(pose, color)

    def _map_couleur(self, couleur_standard):
        # Convertit le nom de couleur complet en lettre utilisée dans .dance et .battle
        mapping = {
            'Rouge':      'R',
            'Bleu':       'B',
            'Bleu Ciel':  'B',
            'Bleu Foncé': 'B',
            'Vert':       'V',
            'Jaune':      'J',
            'Mauve':      'M',
            'Blanc':      'W',
            'Gris':       'G',
            'Noir':       'N',
        }
        return mapping.get(couleur_standard, '')


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
            self.start_btn.setEnabled(False)
            self._thread = _DanceThread(self._connection, self._arbitre, self._dance_loader, nb_mouvements)
            self._thread.score_update.connect(lambda s: self.score_label.setText(str(s)))
            self._thread.finished.connect(lambda: self.start_btn.setEnabled(True))
            self._thread.start()
        except Exception:
            self.statut_label.setText("Erreur : arbitre inaccessible")
            self.statut_label.setStyleSheet("color: red")
