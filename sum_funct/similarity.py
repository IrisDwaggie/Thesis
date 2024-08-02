# NLTK Packages
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

from nltk.stem import PorterStemmer



def similarity(doc1, doc2):
    X_list = word_tokenize(doc1)
    Y_list = word_tokenize(doc2)
    sw = stopwords.words('english')

    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    ps = PorterStemmer()

    l1 = [];
    l2 = []
    porter_stemmer1 = []
    for w in X_set:
        x = ps.stem(w)
        porter_stemmer1.append(x)

    porter_stemmer2 = []
    for w in Y_set:
        x = ps.stem(w)
        porter_stemmer2.append(x)

    a_set = set(porter_stemmer1)
    b_set = set(porter_stemmer2)
    rvector = a_set.union(b_set)
    for w in rvector:
        if w in a_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in b_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    return cosine