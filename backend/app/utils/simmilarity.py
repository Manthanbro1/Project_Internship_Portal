from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(source_text: str, target_texts: list[str]) -> list[float]:
    corpus = [source_text] + target_texts

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]

    return similarities.tolist()
