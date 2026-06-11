from flask import Flask, request, jsonify
import uuid
import datetime

from Battle_Loader import BattleLoader

app = Flask(__name__)

# { robot_id: { 'score': int, 'nombre_pas': int } }
robots_connectes = {}

# Journal d'activité (100 dernières entrées max)
activite = []


def log(message):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    activite.append({"heure": heure, "message": message})
    if len(activite) > 100:
        activite.pop(0)
    print(f"[{heure}] {message}")


@app.route('/', methods=['GET'])
def version():
    return '1.2'

#démare la connection avec un robot et lui donne un identifiant unique
@app.route('/hello', methods=['POST'])
def hello():
    robot_id = str(uuid.uuid4())[:6].upper()
    robots_connectes[robot_id] = {'score': 0, 'nombre_pas': 0}
    log(f"Robot enregistré : {robot_id}")
    return robot_id

#démare la chorégraphie du robot
@app.route('/start', methods=['POST'])
def start():
    donnees = request.get_json()
    robot_id = donnees.get('rid')
    if robot_id not in robots_connectes:
        return jsonify({'erreur': 'Robot inconnu'}), 404
    robots_connectes[robot_id]['score'] = 0
    robots_connectes[robot_id]['nombre_pas'] = 0
    nb_mouvements = BattleLoader.max_steps
    log(f"Chorégraphie démarrée pour {robot_id} ({nb_mouvements} mouvements)")
    return jsonify(0)  # nombre de mouvements — à définir quand le fichier .battle sera chargé

#reçoit un pas à effectuer par le robot et calcule les points obtenus
@app.route('/step', methods=['POST'])
def step():
    donnees = request.get_json()
    robot_id = donnees.get('rid')
    couleur = donnees.get('col', '')
    mouvement_bras = donnees.get('arm', '')
    expression = donnees.get('exp', '')
    if robot_id not in robots_connectes:
        return jsonify({'erreur': 'Robot inconnu'}), 404
    robots_connectes[robot_id]['nombre_pas'] += 1
    points = BattleLoader.score(couleur, mouvement_bras, expression)
    robots_connectes[robot_id]['score'] += points
    log(f"{robot_id} | couleur={couleur} bras={mouvement_bras} expression={expression} -> {points:+d} points "
        f"(total: {robots_connectes[robot_id]['score']})")
    return jsonify(0)  # points — calcul à implémenter dans la branche scoring

#retourne le score du robot
@app.route('/score', methods=['GET'])
def score():
    robot_id = request.args.get('rid')
    if robot_id not in robots_connectes:
        return jsonify({'erreur': 'Robot inconnu'}), 404
    return jsonify(robots_connectes[robot_id]['score'])

#liste tous les robots connectés
@app.route('/robots', methods=['GET'])
def liste_robots():
    return jsonify(robots_connectes)


@app.route('/activite', methods=['GET'])
def get_activite():
    return jsonify(activite)

#déconnecte le robot
@app.route('/bye', methods=['POST'])
def bye():
    donnees = request.get_json()
    robot_id = donnees.get('rid')
    if robot_id in robots_connectes:
        log(f"Robot déconnecté : {robot_id}")
        del robots_connectes[robot_id]
    return '', 204


#chareg un fichier battle grâce a un chemin fourni
@app.route('/battle', methods=['POST'])
def charger_battle():

    donnees = request.get_json()
    path = (donnees or {}).get('path', '').strip()

    if not path:
        return jsonify({'erreur': 'Paramètre manquant'}), 400

    try:
        BattleLoader.load_path(path)
        log(f"Fichier .battle chargé : {path} (MVS={BattleLoader.max_steps})")
        # On retourne le résumé des règles pour que l'UI puisse les afficher
        return jsonify({'resume': BattleLoader.get_summary(), 'mouvements': BattleLoader.max_steps})
    except Exception as e:
        return jsonify({'erreur': f'Fichier introuvable : {path}'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
