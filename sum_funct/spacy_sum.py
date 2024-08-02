#SPACY Packages
import nltk
import spacy #works with meanings and frequency.
from spacy.lang.en.stop_words import STOP_WORDS #common words - a, an, the etc.
from nltk.tokenize import word_tokenize, sent_tokenize  #for tokenizing sentences into individual tokens.
# Load the 'en_core_web_lg' model
nlp = spacy.load('en_core_web_lg')

def spacy_summarizer(article_text):
    nlp=spacy.load('en_core_web_lg') #training model of SpaCy.
    docx = nlp(article_text) #create a document object from input text. nlp() takes string as input and returns a Doc object.

    # Get the text of the Doc object
    text = docx.text
    # Tokenize the text
    words = word_tokenize(text)

    stopWords = list(STOP_WORDS) #creates a list of stop_words.

    # Create a dictionary of words and their frequencies.
    freqTable = dict() #create dictionay that maps each word to its frequency.
    for word in words:
        word = word.lower()
        if word not in stopWords: #If it's a stopword, skip over it.
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(text)
    sentenceValue = dict()
    max_freq = max(freqTable.values()) #freqTable.values() to find sentences with the highest frqencies.
    for word in freqTable.keys(): #to gwt the word in the sentences.
        freqTable[word] = (freqTable[word]/max_freq) #normalize the frequency.

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freqTable.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = freqTable[word]
                    else:
                        sentence_scores[sent] += freqTable[word] #total number of length of words.

    import heapq
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary