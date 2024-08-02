import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Keyword extraction function
from rake_nltk import Rake

def extract_keywords(text):
    # Initialize RAKE
    r = Rake()

    # Extract keywords
    r.extract_keywords_from_text(text)

    # Get ranked keywords
    ranked_keywords = r.get_ranked_phrases()

    # Return top 3 keywords
    return ranked_keywords[:1]

# Function to generate title using GPT-2
import re

def extract_first_sentence(text):
    # Use regex to extract the first sentence
    first_sentence = re.match(r"([^\.!?]+[\.!?])", text)
    if first_sentence:
        return first_sentence.group(0)
    else:
        return ""

# Function to generate title using GPT-2
import re


def extract_title(text):
    # Find the position of the substring "Generate a title based on these keywords:"
    start_index = text.find("Generate a title based on these keywords:")

    if start_index != -1:
        # Extract the text following the substring
        title_text = text[start_index + len("Generate a title based on these keywords:"):]

        # Extract the first sentence from the extracted text
        first_sentence = re.match(r"([^\.!?]+[\.!?])", title_text)

        if first_sentence:
            return first_sentence.group(0)

    return ""


# Function to generate title using GPT-2
def generate_title(text):
    keywords = extract_keywords(text)
    prompt = "Generate a title based on these keywords: " + ", ".join(keywords) + ". "

    # Extract the title sentence from the prompt
    title_sentence = extract_title(prompt)

    return title_sentence