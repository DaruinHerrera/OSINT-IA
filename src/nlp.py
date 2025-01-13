import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from models import DBManager

# Npl model to download
""" nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab') """

def preprocess_text(filepath):
    db_manager = DBManager() # Create an instance of DBManager
    if not db_manager.connect(): # Connects to the database
        return
    
    
    if not filepath:
        return []  # Handle empty filepath

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()  # Read the entire text content
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []  # Handle file not found

    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Removing punctuation marks
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    #print(tokens)
    
    get_key_words_frequency(tokens)
    get_key_phrases_rake_phrases(text)
    get_key_words_tfidf([text]) 
    

def get_key_words_frequency(tokens, top_n=10):
    frequency = Counter(tokens)
    result = frequency.most_common(top_n)
    print(f'Frequency {result}')

def get_key_phrases_rake_phrases(text, top_n=10):
    r = Rake()
    r.extract_keywords_from_text(text)
    result = r.get_ranked_phrases()[:top_n]
    print(f'Key rake {result}')

def get_key_words_tfidf(texts, top_n=10):
    keywords = ["malware", "phishing", "ransomware", 
                "vulnerabilidad", "exploit", "ciberataque", "seguridad informática", 
                "firewall", "antivirus", "criptografía", "ddos", "sql injection",
                "xss", "zero-day", "brecha de seguridad"]

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), vocabulary=keywords) # Filter vocabulary
    tfidf_matrix = vectorizer.fit_transform(texts)

    if tfidf_matrix.nnz == 0:  # Checks if the matrix is empty
        print("None of the cybersecurity keywords were found in the texts.")
        return []

    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray().flatten()

    keywords_tfidf = sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)[:top_n]
    print(f'Key_tfidf {keywords_tfidf}')
    return keywords_tfidf

preprocess_text('../data/results.csv')