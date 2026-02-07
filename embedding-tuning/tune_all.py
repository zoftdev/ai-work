"""Full grid search: model × refs × scoring × threshold. Top 10 by F1 and by accuracy; write results.md."""
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
    score_mean_all,
    score_top3_mean,
    score_weighted_max,
)

REF_V1 = POC_DIR / "eco_ref_sentences.txt"
REF_V2 = Path(__file__).resolve().parent / "eco_ref_sentences_v2.txt"

MODELS = [
    ("MiniLM-L6", "all-MiniLM-L6-v2"),
    ("mpnet-base", "all-mpnet-base-v2"),
    ("bge-small", "BAAI/bge-small-en-v1.5"),
]

SCORERS = [
    ("max", score_max),
    ("top3_mean", score_top3_mean),
    ("mean_all", score_mean_all),
    ("weighted_max", lambda s: score_weighted_max(s, floor=0.25)),
]

REFS = [("v1", REF_V1), ("v2", REF_V2)]
THRESHOLDS = [round(x * 0.01, 2) for x in range(25, 51)]


def main():
    titles, y_true = load_data()
    results = []

    for model_label, model_id in MODELS:
        model = SentenceTransformer(model_id)
        for ref_label, ref_path in REFS:
            ref_sentences = load_ref_sentences(ref_path)
            sims = compute_sims(model, ref_sentences, titles)
            for scoring_name, scorer in SCORERS:
                scores = scorer(sims)
                for thresh in THRESHOLDS:
                    y_pred = (scores >= thresh).tolist()
                    acc, prec, rec, f1 = metrics(y_true, y_pred)
                    results.append({
                        "model": model_label,
                        "refs": ref_label,
                        "scoring": scoring_name,
                        "threshold": thresh,
                        "acc": acc,
                        "prec": prec,
                        "rec": rec,
                        "f1": f1,
                    })

    by_f1 = sorted(results, key=lambda r: (r["f1"], r["acc"]), reverse=True)
    by_acc = sorted(results, key=lambda r: (r["acc"], r["f1"]), reverse=True)

    out = []
    out.append("# Embedding Tuning Results (Full Grid Search)")
    out.append("")
    out.append("## TOP 10 BY F1")
    out.append("")
    out.append("| Rank | Model | Refs | Scoring | Threshold | Acc | Prec | Rec | F1 |")
    out.append("|------|-------|------|---------|-----------|-----|------|-----|-----|")
    for i, r in enumerate(by_f1[:10], 1):
        out.append(f"| {i} | {r['model']} | {r['refs']} | {r['scoring']} | {r['threshold']:.2f} | {r['acc']:.2f} | {r['prec']:.2f} | {r['rec']:.2f} | {r['f1']:.2f} |")
    out.append("")
    out.append("## TOP 10 BY ACCURACY")
    out.append("")
    out.append("| Rank | Model | Refs | Scoring | Threshold | Acc | Prec | Rec | F1 |")
    out.append("|------|-------|------|---------|-----------|-----|------|-----|-----|")
    for i, r in enumerate(by_acc[:10], 1):
        out.append(f"| {i} | {r['model']} | {r['refs']} | {r['scoring']} | {r['threshold']:.2f} | {r['acc']:.2f} | {r['prec']:.2f} | {r['rec']:.2f} | {r['f1']:.2f} |")
    out.append("")
    best = by_f1[0]
    out.append("## RECOMMENDED CONFIG")
    out.append("")
    out.append(f"- **Model:** {best['model']}")
    out.append(f"- **Refs:** {best['refs']}")
    out.append(f"- **Scoring:** {best['scoring']}")
    out.append(f"- **Threshold:** {best['threshold']:.2f}")
    out.append(f"- **Accuracy:** {best['acc']:.2f}")
    out.append(f"- **F1:** {best['f1']:.2f}")
    out.append("")

    out_path = Path(__file__).resolve().parent / "results.md"
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(out_path.read_text(encoding="utf-8"))
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
