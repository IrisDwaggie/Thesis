import re  #for regular expression.
import streamlit as st #for interface.

from sum_funct.Antonyms_funct import get_antonyms
from sum_funct.Synonym_funct import get_synonyms
from sum_funct.grammar import grammar_check, spelling_check, highlight_mistakes
from sum_funct.keywords import extract_keywords
from sum_funct.nltk_sum import nltk_summarizer
from sum_funct.paraphrasing import paraphrasing
from sum_funct.similarity import similarity
from sum_funct.spacy_sum import spacy_summarizer
from sum_funct.sumy_sum import sumy_summarizer
from sum_funct.text_sentiment_funct import analyze_sentiment

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

from sum_funct.title_suggestion import generate_title


def save_pdf(data, filename):
    # Create a canvas
    c = canvas.Canvas(filename, pagesize=letter)

    # Set font and size
    c.setFont("Helvetica", 12)

    # Split the text into lines with proper wrapping
    lines = textwrap.wrap(data, width=80)

    # Set initial y coordinate
    y = 750

    # Write each line to the PDF
    for line in lines:
        c.drawString(100, y, line)
        y -= 15  # Move to the next line

        # Check if we need to start a new page
        if y < 50:
            c.showPage()
            y = 750  # Reset y coordinate for new page

    # Save the PDF
    c.save()

# Set the theme
st.set_page_config(
    page_title="Text processing App",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("./style/styles.css")

def main():
    activities = ["Home", "Summarize Via Text", "Paraphrase Text", "Keyword extractor",
                  "Synonym suggestion", "Antonym suggestion", "Text sentiment analysis",
                  "Grammar check", "Spelling check", "Text title suggestion"]
    st.sidebar.markdown("<h2 class='sidebar-heading'>🧭Navigation Menu🧭</h2>", unsafe_allow_html=True)
    choice = st.sidebar.radio("Select Activity", activities, label_visibility="hidden")

    if choice == 'Home':
        st.write("<h3 class='center-text-home'>📑Welcome to the text processing app home page!📑</h3>", unsafe_allow_html=True)
        st.image("media/NLP_Header.png", use_column_width=True)
        st.markdown("""
            <div class='text-container'>
                <h4 class='text-description-header'>This is a desktop application designed to make working with text easier using artificial intelligence.</h4>
                <p class='text-description'>This program has powerful capabilities for analyzing, processing, and interpreting texts, helping you effectively solve a wide range of problems.</p>
                <h5 class='sub-heading'>What you can do:</h5>
                <ol class='text-list'>
                    <li>Create a summary. This program will help you automatically create a summary using several language models.</li>
                    <li>Selecting keywords. The program is capable of analyzing text to identify keywords.</li>
                    <li>Paraphrasing text. This program is capable of paraphrasing text.</li>
                    <li>Synonym suggestion. This program is capable to suggest synonyms for given word.</li>
                    <li>Antonym suggestion. This program is capable to suggest antonyms for given word.</li>
                    <li>Checking text's sentiment. The program is capable of analyzing text for sentiment.</li>
                    <li>Grammar check. The program is capable of analyzing text for grammar mistakes.</li>
                    <li>Spelling check. The program is capable of analyzing text for spelling mistakes.</li>
                    <li>Title suggestion. The program is capable of analyzing text to make a title.</li>
                </ol>
                <p class='text-description'>Our team works hard to continuously improve and develop the program to provide you with the best text processing tools. Join us today and discover new possibilities in working with text using artificial intelligence!</p>
            </div>
            """, unsafe_allow_html=True)
        st.write("<h3 class='center-text-home'>📖User guide📖</h3>",
                 unsafe_allow_html=True)

        st.markdown("<h2 class='tips-header'>How to change color theme</h2>",
                    unsafe_allow_html=True)
        st.markdown("<h2 class='sidebar-heading'>Step 1. Click on this button, then \"settings\"</h2>", unsafe_allow_html=True)
        st.image("media/Theme 1.png", width=640)
        st.markdown("<h2 class='sidebar-heading'>Step 2. Choose a theme</h2>", unsafe_allow_html=True)
        st.image("media/Theme 2.png", use_column_width=True)

        st.markdown("<h2 class='tips-header'>How to use Application?</h2>",
                    unsafe_allow_html=True)
        st.markdown("<h2 class='sidebar-heading'>Step 1. Choose an option in the navigation bar</h2>",
                    unsafe_allow_html=True)
        st.image("media/UserGuide1.png", width=640)
        st.markdown("<h2 class='sidebar-heading'>Step 2. Input text in text area</h2>",
                    unsafe_allow_html=True)
        st.image("media/UserGuide2.png", width=640)
        st.markdown("<h2 class='sidebar-heading'>Step 3. Choose a language model</h2>",
                    unsafe_allow_html=True)
        st.image("media/UserGuide3.png", width=640)
        st.markdown("<h2 class='sidebar-heading'>Step 4. Push a button to begin processing</h2>",
                    unsafe_allow_html=True)
        st.image("media/UserGuide4.png", width=640)
        st.markdown("<h2 class='sidebar-heading'>Optional Step 5. Save as txt or pdf</h2>",
                    unsafe_allow_html=True)
        st.image("media/UserGuide5.png", width=640)

    if choice == 'Summarize Via Text':
        st.markdown("<h2 class='tips-header'>Summary using NLP</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")

        # Check if the input text is empty
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            # Cleaning of input text.
            article_text = re.sub('\\[[0-9]*\\]', ' ', article_text)  # Any letter enclosed in brackets and is a number.
            article_text = re.sub('[^a-zA-Z.,]', ' ', article_text)  # Any text that's not a letter.
            article_text = re.sub(r"\b[a-zA-Z]\b", '', article_text)  # Any character surrounded by whitespace.
            article_text = re.sub("[A-Z]\Z", '', article_text)  # Any uppercase letter in the end of the text.
            article_text = re.sub(r'\s+', ' ', article_text)  # Whitespace character.

            summary_choice = st.selectbox("Summary Choice", ["NLTK", "SPACY", "Sumy"])

            if summary_choice == 'Sumy':
                num_sentences = st.number_input("Enter the number of sentences for summary(min = 3; max = 10):",
                                                min_value=3,
                                                max_value=10,
                                                value=5)

            if st.button("Summarize Via Text"):
                if summary_choice == 'NLTK':
                    summary_result = nltk_summarizer(article_text)
                elif summary_choice == 'SPACY':
                    summary_result = spacy_summarizer(article_text)
                elif summary_choice == 'Sumy':
                    summary_result = sumy_summarizer(article_text, num_sentences)

                st.write(summary_result)

                wrapped_text = "\n".join(textwrap.wrap(summary_result, width=80))
                st.download_button("Download txt", wrapped_text, file_name="summary.txt")

                pdf_filename = "summary.pdf"
                save_pdf(summary_result, pdf_filename)
                with open(pdf_filename, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="summary.pdf",
                    mime="application/pdf",
                )

    if choice == "Paraphrase Text":
        st.markdown("<h2 class='tips-header'>Paraphrase</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            # cleaning of input text
            article_text = re.sub(r'\\[[0-9]*\\]', ' ', article_text)
            article_text = re.sub('[^a-zA-Z.,]', ' ', article_text)
            article_text = re.sub(r"\b[a-zA-Z]\b", '', article_text)
            article_text = re.sub("[A-Z]\Z", '', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)

            summary_choice = st.selectbox("Paraphrase Choice", ["seq2seq"])
            if st.button("Paraphrase Text"):
                paraphrase_result = paraphrasing(article_text)
                st.write("PARAPHRASE OF THE GIVEN SENTENCE")
                st.write(paraphrase_result)
                st.write("SIMILARITY BETWEEN ORIGINAL SENTENCE AND PARAPHRASED SENTENCE")
                similarity_score = similarity(article_text, paraphrase_result)
                similarity_percent = similarity_score * 100
                st.write(f"Similarity: {similarity_percent:.2f}%")

    if choice == 'Keyword extractor':
        st.markdown("<h2 class='tips-header'>Keyword extractor</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            if st.button("Extract keywords"):
                keywords = extract_keywords(article_text)
                for keyword, freq in keywords:
                    st.write(keyword, freq)

    if choice == 'Synonym suggestion':
        st.markdown("<h2 class='tips-header'>Synonym suggestion</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_input("Enter word Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            if st.button("Get synonyms"):
                synonyms = get_synonyms(article_text)
                for synonym in synonyms:
                    st.write(synonym)

    if choice == 'Antonym suggestion':
        st.markdown("<h2 class='tips-header'>Antonym suggestion</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_input("Enter word Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            if st.button("Get antonyms"):
                antonyms = get_antonyms(article_text)
                for antonym in antonyms:
                    st.write(antonym)

    if choice == 'Text sentiment analysis':
        st.markdown("<h2 class='tips-header'>Text sentiment analysis</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            # cleaning of input text
            article_text = re.sub(r'\\[[0-9]*\\]', ' ', article_text)
            article_text = re.sub('[^a-zA-Z.,]', ' ', article_text)
            article_text = re.sub(r"\b[a-zA-Z]\b", '', article_text)
            article_text = re.sub("[A-Z]\Z", '', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)

            if st.button("Analyze"):
                sentiment = analyze_sentiment(article_text)
                st.write("Sentiment:", sentiment)

    if choice == 'Grammar check':
        st.markdown("<h2 class='tips-header'>Grammar check</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            if st.button("Check Grammar"):
                grammar_mistakes = grammar_check(article_text)
                if grammar_mistakes:
                    st.write("Grammar mistakes found:")
                    highlighted_text = highlight_mistakes(article_text, grammar_mistakes)
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                    for mistake in grammar_mistakes:
                        st.write(f"- {mistake[2]}")
                else:
                    st.write("No grammar mistakes found.")

    if choice == 'Spelling check':
        st.markdown("<h2 class='tips-header'>Spelling check</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            if st.button("Check Spelling"):
                spelling_mistakes = spelling_check(article_text)
                if spelling_mistakes:
                    st.write("Spelling mistakes found:")
                    highlighted_text = article_text
                    for mistake in spelling_mistakes:
                        word, comment = mistake
                        highlighted_text = highlighted_text.replace(word, f"<u>{word}</u>")
                        highlighted_text = highlighted_text.replace(word.capitalize(), f"<u>{word.capitalize()}</u>")
                        highlighted_text = highlighted_text.replace(word.upper(), f"<u>{word.upper()}</u>")
                        st.write(f"- {comment}")
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                else:
                    st.write("No spelling mistakes found.")

    if choice == 'Text title suggestion':
        st.markdown("<h2 class='tips-header'>Text title suggestion</h2>",
                    unsafe_allow_html=True)
        article_text = st.text_area("Enter Text Here")
        if not article_text.strip():
            st.warning("Please enter some text before proceeding.")
        else:
            if st.button("Suggest a title"):
                # Generate title
                suggested_title = generate_title(article_text)
                st.success("Suggested Title: " + suggested_title)

if __name__=='__main__':
    main()