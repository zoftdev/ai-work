"""Compare scoring strategies: max, top3_mean, mean_all, weighted_max. Report best threshold + metrics per strategy × ref set."""
from pathlib import Path

from sentence_transformers import SentenceTransformer

from _embed_utils import (
    POC_DIR,
    compute_sims,
    load_data,
    load_ref_sentences,
    metrics,
    score_max,
    score_mean_all,
    score_top3_mean,
    score_weighted_max,
)

REF_V1 = POC_DIR / "eco_ref_sentences.txt"
REF_V2 = Path(__file__).resolve().parent / "eco_ref_sentences_v2.txt"

SCORERS = [
    ("max", score_max),
    ("top3_mean", score_top3_mean),
    ("mean_all", score_mean_all),
    ("weighted_max", lambda s: score_weighted_max(s, floor=0.25)),
]

THRESHOLDS = [round(x * 0.01, 2) for x in range(25, 51)]


def best_for_scores(scores, y_true):
    """Return (best_threshold, best_f1, acc, prec, rec) at best F1 threshold."""
    best_f1 = -1.0
    best_t = None
    best_acc = best_prec = best_rec = 0.0
    for t in THRESHOLDS:
        y_pred = (scores >= t).tolist()
        acc, prec, rec, f1 = metrics(y_true, y_pred)
        if f1 > best_f1:
            best_f1 = f1
            best_t = t
            best_acc, best_prec, best_rec = acc, prec, rec
    return best_t, best_f1, best_acc, best_prec, best_rec


def main():
    titles, y_true = load_data()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    for ref_name, ref_path in [("v1", REF_V1), ("v2", REF_V2)]:
        ref_sentences = load_ref_sentences(ref_path)
        sims = compute_sims(model, ref_sentences, titles)
        print(f"\n=== Ref set: {ref_path.name} ({len(ref_sentences)} refs) ===")
        for name, scorer in SCORERS:
            scores = scorer(sims)
            t, f1, acc, prec, rec = best_for_scores(scores, y_true)
            print(f"  {name:12}  best_threshold={t:.2f}  Acc={acc:.2f}  Prec={prec:.2f}  Rec={rec:.2f}  F1={f1:.2f}")


if __name__ == "__main__":
    main()
