from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model

def score_exact(actual: str, expected: str) -> float:
    """For exact string match (case-insensitive)"""
    return 1.0 if actual.lower().strip() == expected.lower().strip() else 0.0

def score_semantic(actual: str, expected: str, threshold: float = 0.8) -> float:
    """For semantic similarity using sentence embeddings."""
    model = get_embedding_model()
    embeddings = model.encode([actual, expected])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]]).item()
    return(float(similarity))

