"""
Test de connexion entre le joueur et l'arbitre.
Lance d'abord le serveur : python serveur.py
Puis dans un autre terminal : python test_serveur.py
"""

import requests

BASE = 'http://localhost:8000'


def sep(titre):
    print(f"\n{'='*40}\n  {titre}\n{'='*40}")


# 1. Ping
sep("1. Ping (GET /)")
r = requests.get(f'{BASE}/')
print(f"  [{r.status_code}] → {r.text.strip()}")
assert r.text.strip() == '1.2'

# 2. Enregistrement
sep("2. Enregistrement du robot (POST /hello)")
r = requests.post(f'{BASE}/hello')
rid = r.text.strip()
print(f"  [{r.status_code}] → RID = {rid}")
assert r.status_code == 200

# 3. Démarrage
sep("3. Démarrage chorégraphie (POST /start)")
r = requests.post(f'{BASE}/start', json={'rid': rid})
print(f"  [{r.status_code}] → {r.json()} mouvements")
assert r.status_code == 200

# 4. Envoi de pas
sep("4. Envoi de pas (POST /step)")
for col, arm, exp in [('R', 'ALU+ARU', 'XNG'), ('B', '', 'XSD'), ('N', 'ALB', 'XNT')]:
    r = requests.post(f'{BASE}/step', json={'rid': rid, 'col': col, 'arm': arm, 'exp': exp})
    print(f"  [{r.status_code}] col={col} arm={arm} exp={exp} → {r.json()} pts")
    assert r.status_code == 200

# 5. Score
sep("5. Score (GET /score)")
r = requests.get(f'{BASE}/score', params={'rid': rid})
print(f"  [{r.status_code}] → score = {r.json()}")
assert r.status_code == 200

# 6. Déconnexion
sep("6. Déconnexion (POST /bye)")
r = requests.post(f'{BASE}/bye', json={'rid': rid})
print(f"  [{r.status_code}] → OK")
assert r.status_code == 204

# 7. Vérification robot supprimé
sep("7. Robot supprimé (doit retourner 404)")
r = requests.get(f'{BASE}/score', params={'rid': rid})
print(f"  [{r.status_code}] → {r.json()}")
assert r.status_code == 404

print("\n✓ Connexion arbitre-joueur OK\n")
