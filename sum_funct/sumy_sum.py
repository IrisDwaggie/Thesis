#Sumy Packages
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def sumy_summarizer(text, num_sentences):
    # Parse the text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Initialize the summarizer
    summarizer = LsaSummarizer()

    # Get the summary
    summary = summarizer(parser.document, num_sentences)

    # Join the sentences to form the summary
    summary_text = " ".join([str(sentence) for sentence in summary])

    return summary_text