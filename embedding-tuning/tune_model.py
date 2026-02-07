"""Compare embedding models: MiniLM, mpnet-base, bge-small. Report accuracy, F1, speed, model size."""
import time
from pathlib import Path

from sentence_transformers import SentenceTransformer

from _embed_utils import (
    POC_DIR,
    compute_sims,
    load_data,
    load_ref_sentences,
    metrics,
    score_max,
)

REF_V2 = Path(__file__).resolve().parent / "eco_ref_sentences_v2.txt"

MODELS = [
    ("all-MiniLM-L6-v2", "MiniLM-L6", "80MB", 0.34),
    ("all-mpnet-base-v2", "mpnet-base", "420MB", 0.34),
    ("BAAI/bge-small-en-v1.5", "bge-small", "130MB", 0.34),
]


def main():
    titles, y_true = load_data()
    ref_sentences = load_ref_sentences(REF_V2)

    print("Model           Size    Threshold  Accuracy  Precision  Recall  F1     Time(s)")
    print("-" * 75)
    for model_id, label, size, thresh in MODELS:
        model = SentenceTransformer(model_id)
        t0 = time.perf_counter()
        sims = compute_sims(model, ref_sentences, titles)
        elapsed = time.perf_counter() - t0
        scores = score_max(sims)
        y_pred = (scores >= thresh).tolist()
        acc, prec, rec, f1 = metrics(y_true, y_pred)
        print(f"{label:14}  {size:6}  {thresh:.2f}        {acc:.2f}       {prec:.2f}        {rec:.2f}     {f1:.2f}   {elapsed:.2f}")


if __name__ == "__main__":
    main()
