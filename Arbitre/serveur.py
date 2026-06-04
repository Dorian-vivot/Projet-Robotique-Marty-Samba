from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# { robot_id: { 'score': int, 'nombre_pas': int } }
robots_connectes = {}


@app.route('/', methods=['GET'])
def version():
    return '1.2'


@app.route('/hello', methods=['POST'])
def hello():
    robot_id = str(uuid.uuid4())[:6].upper()
    robots_connectes[robot_id] = {'score': 0, 'nombre_pas': 0}
    print(f"[+] Robot enregistré : {robot_id}")
    return robot_id


@app.route('/start', methods=['POST'])
def start():
    donnees = request.get_json()
    robot_id = donnees.get('rid')
    if robot_id not in robots_connectes:
        return jsonify({'erreur': 'Robot inconnu'}), 404
    robots_connectes[robot_id]['score'] = 0
    robots_connectes[robot_id]['nombre_pas'] = 0
    print(f"[>] Chorégraphie démarrée pour {robot_id}")
    return jsonify(0)  # nombre de mouvements — à définir quand le fichier .battle sera chargé


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
    print(f"[~] {robot_id} | couleur={couleur} bras={mouvement_bras} expression={expression}")
    return jsonify(0)  # points — calcul à implémenter dans la branche scoring


@app.route('/score', methods=['GET'])
def score():
    robot_id = request.args.get('rid')
    if robot_id not in robots_connectes:
        return jsonify({'erreur': 'Robot inconnu'}), 404
    return jsonify(robots_connectes[robot_id]['score'])


@app.route('/robots', methods=['GET'])
def liste_robots():
    return jsonify(robots_connectes)


@app.route('/bye', methods=['POST'])
def bye():
    donnees = request.get_json()
    robot_id = donnees.get('rid')
    if robot_id in robots_connectes:
        print(f"[-] Robot déconnecté : {robot_id}")
        del robots_connectes[robot_id]
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
