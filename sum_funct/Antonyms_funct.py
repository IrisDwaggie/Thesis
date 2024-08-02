import spacy
from spacy.tokens import Token
from nltk.corpus import wordnet as wn

def get_antonyms(word):
    antonyms = []

    # Registering wordnet extension attribute
    Token.set_extension('wordnet', getter=lambda token: wn.synsets(token.text),force=True)

    # Using spaCy for antonym extraction
    nlp = spacy.load("en_core_web_lg")
    token = nlp(word)
    for synset in token[0]._.wordnet:
        for lemma in synset.lemmas():
            for antonym in lemma.antonyms():
                antonyms.append(antonym.name())

    # Using NLTK for antonym extraction
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            for antonym in lemma.antonyms():
                antonyms.append(antonym.name())

    return set(antonyms)