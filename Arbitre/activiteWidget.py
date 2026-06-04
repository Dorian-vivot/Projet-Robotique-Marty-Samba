import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer

BASE = 'http://localhost:8000'


class ActiviteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self._timer = QTimer()
        self._timer.timeout.connect(self._rafraichir)
        self._timer.start(2000)
        self._rafraichir()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        journal_group = QGroupBox("Journal d'activité")
        journal_layout = QVBoxLayout()

        self.journal = QTextEdit()
        self.journal.setReadOnly(True)
        journal_layout.addWidget(self.journal)

        self.refresh_btn = QPushButton("Rafraîchir")
        self.refresh_btn.clicked.connect(self._rafraichir)
        journal_layout.addWidget(self.refresh_btn)

        journal_group.setLayout(journal_layout)
        layout.addWidget(journal_group)

    def _rafraichir(self):
        try:
            r = requests.get(f'{BASE}/activite', timeout=1)
            entrees = r.json()
            texte = '\n'.join(f"[{e['heure']}] {e['message']}" for e in entrees)
            self.journal.setText(texte)
        except Exception:
            self.journal.setText("Serveur inactif")
