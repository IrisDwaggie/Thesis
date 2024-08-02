import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy

# Download NLTK resources (required only for the first run)
nltk.download('vader_lexicon')

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Function to perform sentiment analysis
def analyze_sentiment(text):
    # Tokenize the text using spaCy
    doc = nlp(text)
    # Initialize SentimentIntensityAnalyzer from NLTK
    sid = SentimentIntensityAnalyzer()
    # Get sentiment scores for the text using NLTK's VADER
    compound_score = sid.polarity_scores(text)['compound']
    # Classify sentiment based on compound score
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment