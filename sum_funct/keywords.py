import re
import spacy
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


def extract_keywords(article_text):
    # Cleaning of input text
    article_text = re.sub(r'\\[[0-9]*\\]', ' ', article_text)
    article_text = re.sub('[^a-zA-Z.,]', ' ', article_text)
    article_text = re.sub(r"\b[a-zA-Z]\b", '', article_text)
    article_text = re.sub("[A-Z]\Z", '', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Tokenizing using NLTK
    tokens = word_tokenize(article_text)

    # Removing punctuation marks
    tokens = [word for word in tokens if word not in string.punctuation]

    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Counting word frequency
    word_freq = Counter(filtered_tokens)

    # Using SpaCy for part-of-speech tagging
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(article_text)

    # Extracting nouns and adjectives
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'ADJ']]

    # Combining NLTK and SpaCy results
    for word, freq in word_freq.items():
        if word in keywords:
            keywords.remove(word)
            keywords.extend([word] * freq)

    # Returning keywords with frequency rates as list of tuples
    return [(word, freq) for word, freq in word_freq.most_common(10)]