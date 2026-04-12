from collections.abc import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(source_text: str, target_texts: list[str]) -> list[float]:
    source_text = (source_text or "").strip()
    target_texts = [text.strip() for text in target_texts]

    if not source_text or not any(target_texts):
        return [0.0 for _ in target_texts]

    corpus = [source_text] + target_texts
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    vectors = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]
    return similarities.tolist()


def overlap_ratio(source_items: Iterable[str], target_items: Iterable[str]) -> float:
    source_set = {item.strip().lower() for item in source_items if item and item.strip()}
    target_set = {item.strip().lower() for item in target_items if item and item.strip()}

    if not source_set or not target_set:
        return 0.0

    common = source_set & target_set
    return len(common) / len(source_set | target_set)
