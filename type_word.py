import spacy

# Assurez-vous d'avoir installé le modèle français :
# pip install spacy
# python -m spacy download fr_core_news_sm

# Charge le modèle de langue français
nlp = spacy.load("fr_core_news_sm")


def pos_tag(word: str):
    """
    Renvoie le type grammatical (part-of-speech) d'un mot français.
    :param word: mot à analyser
    :return: tuple (texte, étiquette universelle, étiquette fine)
    """
    doc = nlp(word)
    # On ne s'attend ici qu'à un seul token
    token = doc[0]
    return token.text, token.pos_, token.tag_


if __name__ == "__main__":
    print("Entrez un mot français (ou 'exit' pour quitter) :")
    while True:
        mot = input("> ").strip()
        if mot.lower() == 'exit':
            break
        texte, pos, tag = pos_tag(mot)
        print(f"Mot: {texte}\nPart-of-speech universelle: {pos}\nÉtiquette fine: {tag}\n")