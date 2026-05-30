from flask import Flask, jsonify
import uuid

app = Flask(__name__)

# Dictionnaire des robots connus : { identifiant : infos }
robots = {}

@app.route("/", methods=["GET"])
def version():
    # Sert juste à vérifier que le serveur répond. Renvoie le numéro de version.
    return "1.2"

@app.route("/hello", methods=["POST"])
def hello():
    # Génère un identifiant unique pour le robot et l'enregistre
    rid = str(uuid.uuid4())[:6]      # ex : "a1b2c3"
    robots[rid] = {"score": 0}       # on initialise son score à 0
    print(f"Nouveau robot enregistré : {rid}")
    return rid

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)