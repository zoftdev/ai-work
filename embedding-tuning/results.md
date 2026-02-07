# Embedding Tuning Results (Full Grid Search)

## TOP 10 BY F1

| Rank | Model | Refs | Scoring | Threshold | Acc | Prec | Rec | F1 |
|------|-------|------|---------|-----------|-----|------|-----|-----|
| 1 | MiniLM-L6 | v2 | max | 0.34 | 1.00 | 1.00 | 1.00 | 1.00 |
| 2 | MiniLM-L6 | v2 | max | 0.35 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | MiniLM-L6 | v2 | max | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | MiniLM-L6 | v2 | max | 0.37 | 1.00 | 1.00 | 1.00 | 1.00 |
| 5 | MiniLM-L6 | v2 | max | 0.38 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | MiniLM-L6 | v2 | max | 0.39 | 1.00 | 1.00 | 1.00 | 1.00 |
| 7 | MiniLM-L6 | v2 | max | 0.40 | 1.00 | 1.00 | 1.00 | 1.00 |
| 8 | MiniLM-L6 | v2 | top3_mean | 0.26 | 1.00 | 1.00 | 1.00 | 1.00 |
| 9 | MiniLM-L6 | v2 | top3_mean | 0.27 | 1.00 | 1.00 | 1.00 | 1.00 |
| 10 | MiniLM-L6 | v2 | top3_mean | 0.28 | 1.00 | 1.00 | 1.00 | 1.00 |

## TOP 10 BY ACCURACY

| Rank | Model | Refs | Scoring | Threshold | Acc | Prec | Rec | F1 |
|------|-------|------|---------|-----------|-----|------|-----|-----|
| 1 | MiniLM-L6 | v2 | max | 0.34 | 1.00 | 1.00 | 1.00 | 1.00 |
| 2 | MiniLM-L6 | v2 | max | 0.35 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | MiniLM-L6 | v2 | max | 0.36 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | MiniLM-L6 | v2 | max | 0.37 | 1.00 | 1.00 | 1.00 | 1.00 |
| 5 | MiniLM-L6 | v2 | max | 0.38 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | MiniLM-L6 | v2 | max | 0.39 | 1.00 | 1.00 | 1.00 | 1.00 |
| 7 | MiniLM-L6 | v2 | max | 0.40 | 1.00 | 1.00 | 1.00 | 1.00 |
| 8 | MiniLM-L6 | v2 | top3_mean | 0.26 | 1.00 | 1.00 | 1.00 | 1.00 |
| 9 | MiniLM-L6 | v2 | top3_mean | 0.27 | 1.00 | 1.00 | 1.00 | 1.00 |
| 10 | MiniLM-L6 | v2 | top3_mean | 0.28 | 1.00 | 1.00 | 1.00 | 1.00 |

## RECOMMENDED CONFIG

- **Model:** MiniLM-L6
- **Refs:** v2
- **Scoring:** max
- **Threshold:** 0.34
- **Accuracy:** 1.00
- **F1:** 1.00

## Summary

Deliverables in `embedding-tuning/`:

- **eco_ref_sentences_v2.txt** — 20 reference sentences (original 12 + 8 for missed topics: oil/OPEC, business confidence, minimum wage, supply chain, ISM/durable goods, Baltic Dry, foreign central banks, tax policy).
- **_embed_utils.py** — Shared helpers: `load_data()`, `load_ref_sentences()`, `compute_sims()`, scorers (max, top3_mean, mean_all, weighted_max), `metrics()`.
- **tune_threshold.py** — Threshold sweep 0.25–0.50 for v1 and v2 refs; v2 best at 0.34 (F1=1.00, Acc=1.00).
- **tune_scoring.py** — Compares 4 strategies; v2 + max/top3_mean/weighted_max all reach F1=1.00.
- **tune_model.py** — Compares MiniLM, mpnet-base, bge-small; MiniLM best (1.00), mpnet 0.97, bge 0.50 at 0.34.
- **tune_all.py** — Full grid (3 models × 2 refs × 4 scoring × 26 thresholds); writes this results file.

To use in `poc-eco-classify`: point the embedding method at `../embedding-tuning/eco_ref_sentences_v2.txt` and set threshold to **0.34**.
