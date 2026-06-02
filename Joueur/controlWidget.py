from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QProgressBar, QPushButton, QSizePolicy, QSlider, QVBoxLayout, QWidget

from martyConnection import MartyConnection

class ControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._connection = MartyConnection()
        self._connection.connected.connect(self._onConnected)
        self._connection.disconnected.connect(self._onDisconnected)
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
        self.color_text = QLabel("Bleu")
        self.color_text.setStyleSheet("color: blue")
        color_hbox.addWidget(self.color_label)
        color_hbox.addWidget(self.color_text)
        color_hbox.addStretch()
        state_hbox.addLayout(color_hbox)

        self.disconnect_button = QPushButton("Se déconnecter")
        self.disconnect_button.clicked.connect(self._onDisconnectButton)
        state_hbox.addWidget(self.disconnect_button)
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
        
        other_group = QGroupBox("Autres")
        other_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        # Ajout des GroupBox
        self.top_layout.addWidget(state_group)
        self.top_layout.addWidget(connexion_group)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(other_group)

        self._setStatusWidgets(False)

    def _onDisconnected(self):
        self._setStatusWidgets(False)

    def _onConnected(self):
        self._setStatusWidgets(True)
        
    def _setStatusWidgets(self, isConnected : bool):
        if isConnected:
            self.isConnected_status_text.setText("Connecté")
            self.isConnected_status_text.setStyleSheet("color: green")
            self.ip_text.setText(self._connection.getIp())
            self.disconnect_button.setEnabled(True)
        else:
            self.isConnected_status_text.setText("Déconnecté")
            self.isConnected_status_text.setStyleSheet("color: red")
            self.ip_text.setText("Non connecté")
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
                self.isConnected_status_text.setText("Échec")
                self.isConnected_status_text.setStyleSheet("color: red")
                QMessageBox.critical(self, "Erreur de connexion", f"La connexion à {ip_address} à échouée.")
        else:
            QMessageBox.warning(self, "Attention", "Veuillez saisir une adresse IP avant la connection.")

    def _onDisconnectButton(self):
        self._connection.disconnect()
    
    def _onAutoConnectClick(self):
        selected_items = self.marty_list.selectedItems()

        if selected_items:
            selected_item = selected_items[0]
            ip_address = selected_item.data(Qt.ItemDataRole.UserRole)
            # TODO : initialiser la connection avec cette adresse IP
                




        

