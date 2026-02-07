"""Grid search threshold 0.25–0.50 (step 0.01) for v1 and v2 refs; report best F1 and best accuracy."""
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

REF_V1 = POC_DIR / "eco_ref_sentences.txt"
REF_V2 = Path(__file__).resolve().parent / "eco_ref_sentences_v2.txt"


def run_ref_set(name: str, ref_path: Path, titles, y_true, model):
    ref_sentences = load_ref_sentences(ref_path)
    n_refs = len(ref_sentences)
    sims = compute_sims(model, ref_sentences, titles)
    scores = score_max(sims)

    print(f"\nReference set: {ref_path.name} ({n_refs} refs)")
    print("Threshold  Accuracy  Precision  Recall  F1")
    best_f1 = -1.0
    best_f1_t = None
    best_acc = -1.0
    best_acc_t = None
    for t in [round(x * 0.01, 2) for x in range(25, 51)]:
        y_pred = (scores >= t).tolist()
        acc, prec, rec, f1 = metrics(y_true, y_pred)
        if f1 > best_f1:
            best_f1 = f1
            best_f1_t = t
        if acc > best_acc:
            best_acc = acc
            best_acc_t = t
        print(f"{t:.2f}       {acc:.2f}       {prec:.2f}        {rec:.2f}     {f1:.2f}")
    print(f"Best F1: threshold={best_f1_t}, F1={best_f1:.2f}")
    print(f"Best Accuracy: threshold={best_acc_t}, accuracy={best_acc:.2f}")
    return best_f1_t, best_acc_t, best_f1, best_acc


def main():
    titles, y_true = load_data()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    run_ref_set("v1", REF_V1, titles, y_true, model)
    run_ref_set("v2", REF_V2, titles, y_true, model)


if __name__ == "__main__":
    main()
