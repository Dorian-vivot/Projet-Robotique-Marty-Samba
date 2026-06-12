from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QProgressBar, QPushButton, QSizePolicy, QSlider, QVBoxLayout, QWidget

from martyConnection import MartyConnection

"""
Classe qui permet de gérer l'interface (Gestion des boutons, mise à jour des champs, Gestion des signaux, etc)
"""
class ControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._connection = MartyConnection()
        self._connection.connected.connect(self._onConnected)
        self._connection.disconnected.connect(self._onDisconnected)
        self._connection.connection_lost.connect(self._onConnectionLost)
        self._connection.battery_update.connect(self._updateBatteryLevel)
        self._connection.color_update.connect(self._updateColor)
        self._build_ui()

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.top_layout = QHBoxLayout()

        # Groupe Box état du robot
        state_group = QGroupBox("État du robot")
        state_group.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.MinimumExpanding)
        state_hbox = QVBoxLayout()

        # ------ Groupe - Etat du robot ------

        # Statut de connexion
        isConnected_hbox = QHBoxLayout()
        self.isConnected_status_label = QLabel("Statut de connection : ")
        self.isConnected_status_text = QLabel()
        isConnected_hbox.addWidget(self.isConnected_status_label)
        isConnected_hbox.addWidget(self.isConnected_status_text)
        isConnected_hbox.addStretch()
        state_hbox.addLayout(isConnected_hbox)
        
        # Adresse IP du robot connecté 
        ip_hbox = QHBoxLayout()
        self.ip_label = QLabel("Adresse IP : ")
        self.ip_text = QLabel()
        ip_hbox.addWidget(self.ip_label)
        ip_hbox.addWidget(self.ip_text)
        ip_hbox.addStretch()
        state_hbox.addLayout(ip_hbox)

        # Niveau de batterie du robot
        battery_hbox = QHBoxLayout()
        self.battery_label = QLabel("Niveau de batterie : ")
        self.battery_bar = QProgressBar()
        self.battery_bar.setRange(0,100)
        self.battery_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #aaa;
                border-radius: 4px;
                background-color: #e0e0e0;
                text-align: center;
                font-size: 11px;
                color: black;
            }
            QProgressBar::chunk {
                background-color: green;
                border-radius: 4px;
            }
        """)
        battery_hbox.addWidget(self.battery_label)
        battery_hbox.addWidget(self.battery_bar)
        battery_hbox.addStretch()
        state_hbox.addLayout(battery_hbox)

        # Couleur de la plaque 
        color_hbox = QHBoxLayout()
        self.color_label = QLabel("Couleur de la plaque : ")
        self.color_text = QLabel("Aucune")
        self.color_text.setStyleSheet("color: gray")
        color_hbox.addWidget(self.color_label)
        color_hbox.addWidget(self.color_text)
        color_hbox.addStretch()
        state_hbox.addLayout(color_hbox)

        self.disconnect_button = QPushButton("Se déconnecter")
        self.disconnect_button.clicked.connect(self._onDisconnectButton)
        state_hbox.addWidget(self.disconnect_button)

        self.get_color_button = QPushButton("Lire la couleur aux pieds")
        self.get_color_button.clicked.connect(self._onGetColorButton)
        state_hbox.addWidget(self.get_color_button)

        state_hbox.addStretch()

        # Groupe Box de connexion
        connexion_group = QGroupBox("Connexion au Robot")
        connexion_group.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Expanding)
        connexion_hbox = QVBoxLayout()

        # ------ Groupe - Connexion (Top) : Saisie manuelle ------
        connection_top_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        connection_top_layout.addLayout(input_layout)

        # Création du label
        self.label_input_ip = QLabel("Saisir IP : ")
        input_layout.addWidget(self.label_input_ip)

        # Création de l'input
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("Adresse IP de Marty (ex : 192.168.1.12)")
        input_layout.addWidget(self.input_ip)

        # Création du boutton de connexion
        self.connexion_button = QPushButton("Se connecter")
        self.connexion_button.clicked.connect(self._onConnectClick)
        connection_top_layout.addWidget(self.connexion_button)

        # ------ Groupe - Connexion (Bottom) : Recherche automatique ------
        bottom_layout = QVBoxLayout()

        # Liste déroulante des robots
        self.marty_list = QListWidget()
        self.marty_list.setMaximumHeight(60)

        # Exemple à supprimer 
        test_ROBOT = QListWidgetItem("Marty - 192.168.1.1")
        test_ROBOT.setData(Qt.ItemDataRole.UserRole,"192.168.1.1")

        self.marty_list.addItem(test_ROBOT)
        bottom_layout.addWidget(self.marty_list)

        # Création du boutton de recherche automatique
        self.scan_button = QPushButton("Lancer le scan") # TODO : Pour lancer le scan utiliser QThread pour ne pas figer l'UI car la recherche prend du temps puis actualiser la liste des robots
        bottom_layout.addWidget(self.scan_button)

        # Création du boutton de recherche automatique
        self.connexion_button_auto = QPushButton("Connecter")
        self.connexion_button_auto.clicked.connect(self._onAutoConnectClick)
        bottom_layout.addWidget(self.connexion_button_auto)
        bottom_layout.addStretch()
        
        connexion_hbox.addLayout(connection_top_layout)
        connexion_hbox.addLayout(bottom_layout)
        connexion_group.setLayout(connexion_hbox)
        state_group.setLayout(state_hbox)

        # ------ Groupe - Déplacements ------
        movement_group = QGroupBox("Déplacements")
        movement_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        movement_layout = QVBoxLayout()

        # Fléches directionnel
        movements_layout = QGridLayout()
        movements_layout.setSpacing(4)

        # Contrôle des bras
        arms_layout = QHBoxLayout()

        arms_left_group = QGroupBox("Bras gauche")
        arms_left_layout = QVBoxLayout()
        self.btn_alu = QPushButton("ALU — Lever")
        self.btn_alb = QPushButton("ALB — Arrière")
        self.btn_alu.clicked.connect(lambda: self._onArmClick("left", "raise"))
        self.btn_alb.clicked.connect(lambda: self._onArmClick("left", "back"))
        arms_left_layout.addWidget(self.btn_alu)
        arms_left_layout.addWidget(self.btn_alb)
        arms_left_group.setLayout(arms_left_layout)

        arms_right_group = QGroupBox("Bras droit")
        arms_right_layout = QVBoxLayout()
        self.btn_aru = QPushButton("ARU — Lever")
        self.btn_arb = QPushButton("ARB — Arrière")
        self.btn_aru.clicked.connect(lambda: self._onArmClick("right", "raise"))
        self.btn_arb.clicked.connect(lambda: self._onArmClick("right", "back"))
        arms_right_layout.addWidget(self.btn_aru)
        arms_right_layout.addWidget(self.btn_arb)
        arms_right_group.setLayout(arms_right_layout)

        btn_arms_neutral = QPushButton("Bras en position neutres")
        btn_arms_neutral.clicked.connect(self._onArmsNeutral)

        arms_layout.addWidget(arms_left_group)
        arms_layout.addWidget(arms_right_group)
        movement_layout.addLayout(arms_layout)
        movement_layout.addWidget(btn_arms_neutral)

        self.btn_forward   = QPushButton("↑")
        self.btn_forward.clicked.connect(lambda: self._onMoveClick("forward"))
        self.btn_backward  = QPushButton("↓")
        self.btn_backward.clicked.connect(lambda: self._onMoveClick("backward"))
        self.btn_left      = QPushButton("←")
        self.btn_left.clicked.connect(lambda: self._onSidestepClick("left"))
        self.btn_right     = QPushButton("→")
        self.btn_right.clicked.connect(lambda: self._onSidestepClick("right"))
        self.btn_turn_left  = QPushButton("Tourner à Gauche")
        self.btn_turn_left.clicked.connect(lambda:  self._onTurnClick("left"))
        self.btn_turn_right = QPushButton("Tourner à Droite")
        self.btn_turn_right.clicked.connect(lambda: self._onTurnClick("right"))

        movements_layout.addWidget(self.btn_forward,    0, 1)
        movements_layout.addWidget(self.btn_left,       1, 0)
        movements_layout.addWidget(self.btn_right,      1, 2)
        movements_layout.addWidget(self.btn_backward,   2, 1)
        movements_layout.addWidget(self.btn_turn_left,  3, 0)
        movements_layout.addWidget(self.btn_turn_right, 3, 2)
        movement_layout.addLayout(movements_layout)

        # Bouton stop
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self._onStopClick)
        movement_layout.addWidget(self.btn_stop)
        movement_group.setLayout(movement_layout)

        # ------ Groupe - Expressions ------
        expression_group = QGroupBox("Expressions")
        expression_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        expression_layout = QVBoxLayout()

        # Poses des sourcils
        expression_layout.addWidget(QLabel("Sourcils :"))
        poses_grid = QGridLayout()
        poses_grid.setSpacing(4)
        for i, pose in enumerate(["normal", "angry", "excited", "wide", "wiggle"]):
            btn = QPushButton(pose)
            btn.clicked.connect(lambda _, p=pose: self._onEyesPoseClick(p))
            poses_grid.addWidget(btn, i // 3, i % 3)
        expression_layout.addLayout(poses_grid)

        # Raccourcis expressions complètes (pose + couleur LED)
        expression_layout.addWidget(QLabel("Raccourcis :"))
        shortcuts_grid = QGridLayout()
        shortcuts_grid.setSpacing(4)
        shortcuts = [
            ("XNT — Neutre",  "normal",  (128, 128, 128)),
            ("XSD — Triste",  "normal",  (0,   0,   255)),
            ("XNG — Énervé",  "angry",   (255, 0,   0  )),
            ("XHP — Content", "excited", (0,   255, 0  )),
        ]
        for i, (label, pose, color) in enumerate(shortcuts):
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, p=pose, c=color: self._onExpressionShortcut(p, c))
            shortcuts_grid.addWidget(btn, i // 2, i % 2)
        expression_layout.addLayout(shortcuts_grid)

        expression_group.setLayout(expression_layout)

        # ------ Ajout des groupes au layout principal ------
        controls_row = QHBoxLayout()
        controls_row.addWidget(movement_group)
        controls_row.addWidget(expression_group)

        # Ajout des GroupBox
        self.top_layout.addWidget(state_group)
        self.top_layout.addWidget(connexion_group)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(controls_row)
        self.main_layout.addStretch()

        self._setStatusWidgets(False)

    def _onDisconnected(self):
        self._setStatusWidgets(False)

    def _onConnected(self):
        self._setStatusWidgets(True)

    def _onConnectionLost(self):
        self._setStatusWidgets(False)
    
    def _updateBatteryLevel(self, batteryLevel : int):
        self.battery_bar.setValue(batteryLevel)

    def _updateColor(self, colorDetected : str):
        match colorDetected:
            case "Rouge":
                self.color_text.setStyleSheet("color: red")
            case "Vert":
                self.color_text.setStyleSheet("color: green")
            case "Bleu":
                self.color_text.setStyleSheet("color: blue")
            case "Jaune":
                self.color_text.setStyleSheet("color: yellow")
            case "Rose":
                self.color_text.setStyleSheet("color: purple")
            case "Blanc":
                self.color_text.setStyleSheet("color: white")
            case "Gris":
                self.color_text.setStyleSheet("color: gray")
            case "Noir":
                self.color_text.setStyleSheet("color: black")
            case _:
                self.color_text.setStyleSheet("color: gray")
                self.color_text.setText("Aucune")

        self.color_text.setText(colorDetected)
        
        
    def _setStatusWidgets(self, isConnected : bool):
        if isConnected:
            self.isConnected_status_text.setText("Connecté")
            self.isConnected_status_text.setStyleSheet("color: green")
            self.ip_text.setText(self._connection.getIp())
            self.ip_text.setStyleSheet("color: green")
            self.disconnect_button.setEnabled(True)
        else:
            self.isConnected_status_text.setText("Déconnecté")
            self.isConnected_status_text.setStyleSheet("color: red")
            self.ip_text.setText("Non connecté")
            self.ip_text.setStyleSheet("color: gray")
            self.battery_bar.setValue(0)
            self.disconnect_button.setEnabled(False)

    def _onConnectClick(self):
        ip_address = self.input_ip.text().strip()
        if ip_address:
            self.connexion_button.setEnabled(False)
            self.connexion_button.setText("Connexion en cours...")

            self.isConnected_status_text.setText("Tentative de connexion...")
            self.isConnected_status_text.setStyleSheet("color: orange")

            QApplication.processEvents()

            isConnected = self._connection.connect(ip_address)

            self.connexion_button.setEnabled(True)
            self.connexion_button.setText("Se connecter")
            if isConnected:
                QMessageBox.information(self, "Succès", f"Connection réussi à Marty ({ip_address}).")
            else:
                self.isConnected_status_text.setText("Échec de la connexion")
                self.isConnected_status_text.setStyleSheet("color: red")
                QMessageBox.critical(self, "Erreur de connexion", f"La connexion à {ip_address} à échouée.")
        else:
            QMessageBox.warning(self, "Attention", "Veuillez saisir une adresse IP avant la connection.")

    def _onDisconnectButton(self):
        self._connection.disconnect()

    def _onGetColorButton(self):
        if self._connection.isConnected():
            read_color = self._connection.getStandardFootColor()
            if read_color is not None:
                self._updateColor(read_color)
    
    def _onAutoConnectClick(self):
        selected_items = self.marty_list.selectedItems()

        if selected_items:
            selected_item = selected_items[0]
            ip_address = selected_item.data(Qt.ItemDataRole.UserRole)
            # TODO : initialiser la connection avec cette adresse IP

    def _onMoveClick(self, direction: str):
        self._connection.move(direction)

    def _onSidestepClick(self, side: str):
        self._connection.sidestep(side)

    def _onTurnClick(self, direction: str):
        self._connection.turn(direction)

    def _onStopClick(self):
        self._connection.stop()

    def _onArmClick(self, side: str, movement: str):
        self._connection.moveArm(side, movement)

    def _onArmsNeutral(self):
        self._connection.armsNeutral()

    def _onEyesPoseClick(self, pose: str):
        self._connection.setEyesPose(pose)

    def _onExpressionShortcut(self, pose: str, color: tuple):
        self._connection.setExpression(pose, color)