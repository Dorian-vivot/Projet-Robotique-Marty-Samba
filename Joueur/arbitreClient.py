import requests


class ArbitreClient:
    """Client HTTP pour communiquer avec le serveur arbitre."""

    def __init__(self, host='localhost', port=8000):
        self._base = f'http://{host}:{port}'
        self._rid = None

    @property
    def rid(self):
        return self._rid

    def is_connected(self):
        return self._rid is not None

    # ---------- Méthodes API ----------

    def ping(self):
        """Vérifie que le serveur est disponible. Retourne True/False."""
        try:
            r = requests.get(f'{self._base}/', timeout=2)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def hello(self):
        """Enregistre ce robot. Retourne l'identifiant reçu."""
        r = requests.post(f'{self._base}/hello', timeout=2)
        r.raise_for_status()
        self._rid = r.text.strip()
        return self._rid

    def start(self):
        """Déclare le début de la chorégraphie. Retourne le nombre de mouvements à effectuer."""
        self._check_connected()
        r = requests.post(f'{self._base}/start', json={'rid': self._rid}, timeout=2)
        r.raise_for_status()
        return r.json()

    def step(self, col, arm, exp):
        """
        Envoie un pas effectué. Retourne les points obtenus pour ce pas.
        col : couleur détectée (ex: 'G')
        arm : mouvement de bras (ex: 'ALU+ARU' ou 'ALB')
        exp : expression (ex: 'XNG')
        """
        self._check_connected()
        r = requests.post(f'{self._base}/step', json={
            'rid': self._rid,
            'col': col,
            'arm': arm,
            'exp': exp,
        }, timeout=2)
        r.raise_for_status()
        return r.json()

    def score(self):
        """Retourne le score total du robot."""
        self._check_connected()
        r = requests.get(f'{self._base}/score', params={'rid': self._rid}, timeout=2)
        r.raise_for_status()
        return r.json()

    def bye(self):
        """Déconnecte le robot du serveur."""
        if self._rid:
            try:
                requests.post(f'{self._base}/bye', json={'rid': self._rid}, timeout=2)
            except requests.RequestException:
                pass
            finally:
                self._rid = None

    # ---------- Interne ----------

    def _check_connected(self):
        if not self._rid:
            raise RuntimeError("Pas enregistré auprès du serveur (appeler hello() d'abord)")
