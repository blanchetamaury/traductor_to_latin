import spacy
import libpy as lp
import os
import sys
import urllib.parse, urllib.request, json

# Assurez-vous d'avoir installé le modèle français :
# pip install spacy
# python -m spacy download fr_core_news_sm

# Charge le modèle de langue français
nlp = spacy.load("fr_core_news_sm")

def add_csv(name_file, name_fr, genre_fr, pos_fr, latin):
    """
    Ajoute une ligne au CSV : français, genre, POS, latin
    """
    with open(f"{name_file}.csv", "a", encoding="utf-8") as f:
        f.write(f"{name_fr},{genre_fr},{pos_fr},{latin}\n")


def pos_tag(word: str):
    """
    Renvoie (texte, part-of-speech universelle, étiquette fine, genre) pour un mot français
    """
    doc = nlp(word)
    token = doc[0]
    morph = token.morph.to_dict()
    genre = morph.get("Gender", "N/A")  # 'Masc', 'Fem' ou 'N/A'
    return token.text, token.pos_, token.tag_, genre


def get_trad(word: str) -> str:
    """
    Traduit `word` du français vers le latin via translate.googleapis.com
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


if __name__ == "__main__":
    # Importe les entrées CSV (chaque item est un dict avec la clé 'francais')
    rows = lp.import_csv("liste")
    for row in rows:
        # Vous devez extraire le mot français de la ligne
        word_fr = row.get('francais')
        if not isinstance(word_fr, str):
            continue  # ignore les lignes mal formées
        texte, pos, tag, genre = pos_tag(word_fr)
        latin = get_trad(texte)
        add_csv("database", texte, genre, tag, latin)
