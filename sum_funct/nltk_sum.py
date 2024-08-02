#NLTK Packages
import nltk #natural language toolkit - works on the frequency.
from nltk.corpus import stopwords #common words - a, an, the etc.
from nltk.tokenize import word_tokenize, sent_tokenize  #for tokenizing sentences into individual tokens.

#Function for NLTK
def nltk_summarizer(docx):
    stopWords = set(stopwords.words("english")) #language is specified as English.
    words = word_tokenize(docx)   #convert sentences into individual tokens.
    freqTable = dict() #map values to the dictionary data structure.

    for word in words:  #iterate through words.
        word = word.lower()   #change into lowercase.
        if word not in stopWords: #check if it a stopword.
            if word in freqTable: #check if it's already added in frequency table.
                freqTable[word] += 1 #add it in.
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(docx)   #tokenize the document.
    sentenceValue = dict() #create dictionay that maps each word to its frequency.
    max_freq = max(freqTable.values()) #find maximium frequency in dict().
    for word in freqTable.keys(): #iterate through words
        freqTable[word] = (freqTable[word]/max_freq)  #relative frequency - similar to normalizing.

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()): #tokens in lowercase from above mentioned function.
            if word in freqTable.keys(): #if word exists in frquency table.
                if len(sent.split(' ')) < 30: #if sentence is shorter than 30 words.
                    if sent not in sentence_scores.keys(): #if sentence is in scores dictionary.
                        sentence_scores[sent] = freqTable[word] #add the sentence score to the frequency table.
                    else:
                        sentence_scores[sent] += freqTable[word] #add to the total number of length of words.

    import heapq #heap library.
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get) #nlargest is heapq function that is used to find top n elements in a list. Here we find top 8 sentences with the highest scores.
    summary = ' '.join(summary_sentences) #join sentences together.
    return summary