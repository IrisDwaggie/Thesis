import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from collections import Counter

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_lg")

def grammar_check(text):
    doc = nlp(text)
    mistakes = []

    # Check for grammatical errors
    for token in doc:
        if token.pos_ == 'VERB' and token.dep_ == 'ROOT' and token.tag_ != 'VB':
            mistakes.append((token.text, token.idx, f"Possible grammar error: '{token.text}' might be a wrong verb form."))

    return mistakes

def spelling_check(text):
    tokens = word_tokenize(text)
    # Lowercase and remove stopwords
    tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords.words('english')]
    # Count the occurrences of each word
    word_counts = Counter(tokens)
    misspelled_words = []

    # Check for misspelled words
    for word, count in word_counts.items():
        if count <= 2:  # Arbitrary threshold for rare words
            if not wordnet.synsets(word):
                misspelled_words.append((word, f"'{word}' might be a misspelled word."))

    return misspelled_words

def highlight_mistakes(text, mistakes):
    highlighted_text = ""
    current_index = 0
    for mistake in mistakes:
        word, index, comment = mistake
        highlighted_text += text[current_index:index]
        highlighted_text += f"<u>{word}</u>"
        current_index = index + len(word)
    highlighted_text += text[current_index:]
    return highlighted_text