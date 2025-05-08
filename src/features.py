# src/features.py

from sklearn.feature_extraction.text import TfidfVectorizer

def build_tfidf_matrix(documents: list[str], max_features: int = 5000):

    #Facem extractia de caracteristici
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words="english",
        strip_accents="unicode"
    )
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer
