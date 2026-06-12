# Dance Battle — Projet Robotique

Le projet se compose de deux applications indépendantes : **Joueur** (robot) et **Arbitre** (serveur). Le serveur compte les points en fonction des informations du fichier .battle tandis que le joueur charge le fichier .dance qui décrit les mouvements à éffectuer pour une chorégraphie. Au fur et à mesure des mouvements le robot envoie les mouvements effectués au serveur.

```
polytech-3a-robot/
├── Joueur/          # Application robot (PyQt)
├── Arbitre/         # Application serveur (Flask)
└── requirements.txt
```

---

## Installation

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate.bat     # Windows

pip install -r requirements.txt
```

---

## Fonctionnalités

### Application Joueur

- **Connexion au robot** — saisie manuelle d'une adresse IP recherche automatique sur le réseau (TODO)
- **Contrôle manuel** — déplacements et test des expressions directement depuis l'interface
- **Calibration des couleurs** — association d'une couleur détectée par le capteur à une couleur standard (`Noir`, `Mauve`, `Bleu foncé`, `Vert`…)
- **Surveillance en temps réel** — relevé périodique de l'état de la batterie et de la couleur de la plaque sous le robot
- **Chorégraphie** — chargement d'un fichier `.dance` pour visualiser et exécuter une séquence de mouvements
- **Communication serveur** — envoi automatique des données (couleur, bras, expression) à l'arbitre à chaque pas de la chorégraphie

### Application Arbitre

- **Gestion des robots** — liste des robots enregistrés via `POST /hello`
- **Réception des données** — affichage en temps réel des pas reçus de chaque robot
- **Règles de scoring** — chargement d'un fichier `.battle` définissant les points par combinaison (couleur + bras + expression)
- **Scores en direct** — affichage et mise à jour des points de chaque robot au fil de la battle

---

## Formats de fichiers

### `.dance` — Chorégraphie

```
SEQ 1
1U
2R
1L
ACT
N ARU XNG    # sur noir : bras droit levé + air énervé
R XSD        # sur rouge : air triste
```

Mouvements : `<pas><direction>` — `U` avant · `B` arrière · `L` gauche · `R` droite  
Expressions : `XNT` neutre · `XSD` triste · `XNG` énervé · `XHP` content · `XDN` enjoué  
Bras : `ALU/ARU` levé · `ALB/ARB` en arrière

### `.battle` — Règles de points

```
MVS 10
[N]
ALB+ARB=1    # ET : les deux bras en arrière → +1
ALU=-1       # bras gauche levé → -1
[R]
ALU,ARU=1    # OU : au moins un bras levé → +1
XNG=3
```

`+` opérateur ET · `,` opérateur OU · `MVS` nombre de mouvements

---

## API (Robot ↔ Arbitre)

| Méthode | Route    | Description                        |
|---------|----------|------------------------------------|
| `GET`   | `/`      | Vérification du serveur            |
| `POST`  | `/hello` | Enregistrement du robot            |
| `POST`  | `/start` | Démarrage de la chorégraphie       |
| `POST`  | `/step`  | Envoi d'un pas (col, arm, exp)     |
| `GET`   | `/score` | Score total d'un robot             |
| `POST`  | `/bye`   | Déconnexion du robot               |

Toutes les requêtes/réponses sont en **JSON**.
