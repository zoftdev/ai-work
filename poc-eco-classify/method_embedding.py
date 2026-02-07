"""
Sentence embedding classifier for economic news.
Uses all-MiniLM-L6-v2; classifies as economic if max cosine similarity
to reference sentences exceeds threshold.
"""
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


def _load_ref_sentences(ref_file: str) -> list[str]:
    path = Path(ref_file)
    if not path.exists():
        raise FileNotFoundError(f"Reference file not found: {ref_file}")
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return [line.strip() for line in lines if line.strip()]


def classify(
    articles: list[str],
    ref_file: str = "eco_ref_sentences.txt",
    threshold: float = 0.40,
) -> tuple[list[bool], float]:
    """
    Returns (predictions, elapsed_seconds).
    predictions[i] is True if article i is classified as economic.
    Only inference time is measured (model load excluded).
    """
    ref_sentences = _load_ref_sentences(ref_file)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    ref_embeddings = model.encode(ref_sentences)

    import time
    t0 = time.perf_counter()
    article_embeddings = model.encode(articles)
    # (n_articles, dim) @ (dim, n_refs) -> (n_articles, n_refs); cosine sim with normalized vecs
    ref_norm = ref_embeddings / np.linalg.norm(ref_embeddings, axis=1, keepdims=True)
    art_norm = article_embeddings / np.linalg.norm(article_embeddings, axis=1, keepdims=True)
    sims = np.dot(art_norm, ref_norm.T)  # (n_articles, n_refs)
    max_sims = np.max(sims, axis=1)
    predictions = (max_sims > threshold).tolist()
    elapsed = time.perf_counter() - t0
    return predictions, elapsed


def classify_with_scores(
    articles: list[str],
    ref_file: str = "eco_ref_sentences.txt",
    threshold: float = 0.40,
) -> tuple[list[bool], list[float], float]:
    """
    Returns (predictions, max_scores, elapsed_seconds).
    Useful for benchmark to show score in misclassified lines.
    """
    ref_sentences = _load_ref_sentences(ref_file)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    ref_embeddings = model.encode(ref_sentences)

    import time
    t0 = time.perf_counter()
    article_embeddings = model.encode(articles)
    ref_norm = ref_embeddings / np.linalg.norm(ref_embeddings, axis=1, keepdims=True)
    art_norm = article_embeddings / np.linalg.norm(article_embeddings, axis=1, keepdims=True)
    sims = np.dot(art_norm, ref_norm.T)
    max_sims = np.max(sims, axis=1)
    predictions = (max_sims > threshold).tolist()
    elapsed = time.perf_counter() - t0
    return predictions, max_sims.tolist(), elapsed


if __name__ == "__main__":
    import json
    import sys
    import yaml

    data_file = sys.argv[1] if len(sys.argv) > 1 else "sampledata.yaml"
    data = yaml.safe_load(Path(data_file).read_text(encoding="utf-8"))
    titles = [item["title"] for item in data]

    preds, scores, elapsed = classify_with_scores(titles)
    json.dump({"predictions": preds, "scores": scores, "elapsed": elapsed}, sys.stdout)
    sys.stdout.write("\n")
