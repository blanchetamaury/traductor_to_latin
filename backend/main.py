import libpy as lp
import os
from flask import Flask, request, jsonify
import urllib.parse, urllib.request, json
app = Flask(__name__)

@app.route("/trad", methods=["POST"])
def trad():
    payload = request.get_json(force=True)
    fr = payload.get("text", "").strip()
    if not fr:
        return jsonify({"error": "texte vide"}), 400

    base = lp.import_csv("database")
    for entry in base:
        if entry["francais"] == fr:
            return jsonify({"latin": entry["latin"]})

    la = get_trad(fr) or ""
    if la:
        add_csv("database", fr, la)
    return jsonify({"latin": la})

def get_trad(word):
    """
    Translate `word` from French to Latin by calling the public
    translate.googleapis.com HTTP endpoint directly.
    """
    q = urllib.parse.quote(word)
    url = (
        "https://translate.googleapis.com/translate_a/single"
        "?client=gtx"
        "&sl=fr"
        "&tl=la"
        "&dt=t"
        f"&q={q}"
    )
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())
    return data[0][0][0]


def add_csv(name, new1, new2):
    fd_in = os.open(name + ".csv", os.O_WRONLY | os.O_APPEND)
    os.write(fd_in, '\n'.encode() + new1.encode() + ','.encode())
    os.write(fd_in, new2.encode())

if __name__ == "__main__":
    app.run(port=5000)