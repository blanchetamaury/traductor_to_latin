import libpy as lp
import os
import sys
import json, urllib.parse, urllib.request, urllib.error
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/trad", methods=["POST"])
def trad():
    payload = request.get_json(force=True)
    fr = payload.get("text", "").strip()
    if not fr:
        return jsonify({"error": "texte vide"}), 400

    # 1) Cherche dans la base
    base = lp.import_csv("database")
    for entry in base:
        if entry["francais"] == fr:
            return jsonify({"latin": entry["latin"]})

    # 2) Sinon, appelle MyMemory et ajoute à la base
    la = get_trad(fr) or ""
    if la:
        add_csv("database", fr, la)
        # rechargement optionnel : base = lp.import_csv("database")
    return jsonify({"latin": la})

def get_trad(word):
    params = urllib.parse.urlencode({
        "q": word,
        "langpair": "fr|la"
    })
    url = f"https://api.mymemory.translated.net/get?{params}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.load(r)
    except urllib.error.URLError as e:
        print("Erreur réseau :", e)
        return None
    best = data.get("responseData", {}).get("translatedText")
    if best:
        return best.lower()
    for m in data.get("matches", []):
        if m.get("translation"):
            return m["translation"].lower()
    return None


def add_csv(name, new1, new2):
    fd_in = os.open(name + ".csv", os.O_WRONLY | os.O_APPEND)
    os.write(fd_in, '\n'.encode() + new1.encode() + ','.encode())
    os.write(fd_in, new2.encode())

if __name__ == "__main__":
    app.run(port=5000)