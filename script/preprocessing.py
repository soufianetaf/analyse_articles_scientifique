import re
import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Télécharger les ressources nécessaires
nltk.download("punkt")
nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Supprime les balises HTML, caractères spéciaux et ponctuation.
    """
    text = re.sub(r'<.*?>', ' ', text)  # Supprimer HTML
    text = re.sub(r'[^\w\s]', '', text)  # Supprimer ponctuation
    text = re.sub(r'\d+', '', text)  # Supprimer les chiffres
    return text.lower().strip()

def preprocess_text(text):
    """
    Applique le nettoyage, la tokenization, la suppression des stopwords et la lemmatisation.
    """
    text = clean_text(text)
    
    # Tokenization
    words = word_tokenize(text)
    
    # Suppression des stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatisation
    doc = nlp(" ".join(words))
    lemmatized_words = [token.lemma_ for token in doc]
    
    return " ".join(lemmatized_words)

def segment_sentences(text):
    """
    Segmente un texte en phrases.
    """
    return sent_tokenize(text)

if __name__ == "__main__":
    sample_text = "Artificial intelligence (AI) is revolutionizing the world. Machine learning, deep learning, and NLP are key fields!"
    cleaned_text = preprocess_text(sample_text)
    sentences = segment_sentences(sample_text)
    
    print("Texte prétraité:", cleaned_text)
    print("Phrases segmentées:", sentences)
