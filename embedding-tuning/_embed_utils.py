"""Shared helpers for embedding-tuning scripts. Data from ../poc-eco-classify/."""
from pathlib import Path

import numpy as np
import yaml

POC_DIR = Path(__file__).resolve().parent / ".." / "poc-eco-classify"
TARGET = "economic"


def load_data():
    """Load sampledata.yaml and labels; return (titles, y_true). y_true[i] = (answer == economic)."""
    data = yaml.safe_load((POC_DIR / "sampledata.yaml").read_text(encoding="utf-8"))
    titles = [item["title"] for item in data]
    y_true = [item["answer"] == TARGET for item in data]
    return titles, y_true


def load_ref_sentences(ref_path: Path) -> list[str]:
    """Load reference sentences; skip empty lines and lines starting with #."""
    text = ref_path.read_text(encoding="utf-8").strip()
    return [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]


def compute_sims(model, ref_sentences: list[str], titles: list[str]) -> np.ndarray:
    """Return (n_articles, n_refs) cosine similarities."""
    ref_emb = model.encode(ref_sentences)
    art_emb = model.encode(titles)
    ref_norm = ref_emb / np.linalg.norm(ref_emb, axis=1, keepdims=True)
    art_norm = art_emb / np.linalg.norm(art_emb, axis=1, keepdims=True)
    return np.dot(art_norm, ref_norm.T)


def score_max(sims: np.ndarray) -> np.ndarray:
    """Per-article: max similarity (current default)."""
    return np.max(sims, axis=1)


def score_top3_mean(sims: np.ndarray) -> np.ndarray:
    """Per-article: mean of top 3 similarities."""
    top3 = np.sort(sims, axis=1)[:, -3:]
    return np.mean(top3, axis=1)


def score_mean_all(sims: np.ndarray) -> np.ndarray:
    """Per-article: mean of all reference similarities."""
    return np.mean(sims, axis=1)


def score_weighted_max(sims: np.ndarray, floor: float = 0.25) -> np.ndarray:
    """Per-article: max_sim * (1 + 0.1 * count_above_floor)."""
    max_sim = np.max(sims, axis=1)
    count_above = np.sum(sims >= floor, axis=1)
    return max_sim * (1.0 + 0.1 * count_above)


def metrics(y_true: list[bool], y_pred: list[bool]) -> tuple[float, float, float, float]:
    """Returns (accuracy, precision, recall, F1)."""
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

    y_t = np.asarray(y_true, dtype=bool)
    y_p = np.asarray(y_pred, dtype=bool)
    acc = float(accuracy_score(y_t, y_p))
    prec = float(precision_score(y_t, y_p, zero_division=0))
    rec = float(recall_score(y_t, y_p, zero_division=0))
    f1 = float(f1_score(y_t, y_p, zero_division=0))
    return acc, prec, rec, f1
