import spacy
from spacy.tokens import Token
from nltk.corpus import wordnet as wn

def get_synonyms(word):
    synonyms = []

    # Registering wordnet extension attribute
    Token.set_extension('wordnet', getter=lambda token: wn.synsets(token.text), force=True)

    # Using spaCy for synonym extraction
    nlp = spacy.load('en_core_web_lg')
    token = nlp(word)
    for synset in token[0]._.wordnet:
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())

    # Using NLTK for synonym extraction
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())

    return set(synonyms)