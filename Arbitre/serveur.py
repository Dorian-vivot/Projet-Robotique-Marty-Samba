from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# { rid: { 'score': int, 'steps': int } }
robots = {}


@app.route('/', methods=['GET'])
def version():
    return '1.2'


@app.route('/hello', methods=['POST'])
def hello():
    rid = str(uuid.uuid4())[:6].upper()
    robots[rid] = {'score': 0, 'steps': 0}
    print(f"[+] Robot enregistré : {rid}")
    return rid


@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    rid = data.get('rid')
    if rid not in robots:
        return jsonify({'error': 'Robot inconnu'}), 404
    robots[rid]['score'] = 0
    robots[rid]['steps'] = 0
    print(f"[>] Chorégraphie démarrée pour {rid}")
    return jsonify(0)  # nombre de mouvements — à définir quand le fichier .battle sera chargé


@app.route('/step', methods=['POST'])
def step():
    data = request.get_json()
    rid = data.get('rid')
    col = data.get('col', '')
    arm = data.get('arm', '')
    exp = data.get('exp', '')
    if rid not in robots:
        return jsonify({'error': 'Robot inconnu'}), 404
    robots[rid]['steps'] += 1
    print(f"[~] {rid} | col={col} arm={arm} exp={exp}")
    return jsonify(0)  # points — calcul à implémenter dans la branche scoring


@app.route('/score', methods=['GET'])
def score():
    rid = request.args.get('rid')
    if rid not in robots:
        return jsonify({'error': 'Robot inconnu'}), 404
    return jsonify(robots[rid]['score'])


@app.route('/robots', methods=['GET'])
def liste_robots():
    return jsonify(robots)


@app.route('/bye', methods=['POST'])
def bye():
    data = request.get_json()
    rid = data.get('rid')
    if rid in robots:
        print(f"[-] Robot déconnecté : {rid}")
        del robots[rid]
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
