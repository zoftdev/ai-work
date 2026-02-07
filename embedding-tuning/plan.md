# Embedding Tuning: Optimize Economic News Classification Accuracy

## Context

From `poc-eco-classify` benchmark (2026-02-07):

| Metric | Current |
|---|---|
| Accuracy | 0.85 |
| Precision | 1.00 |
| Recall | 0.70 |
| F1 | 0.82 |
| Threshold | 0.40 |

**Problem:** 9 false negatives — all economic articles scored just below threshold.

| Missed Article | Score | Gap |
|---|---|---|
| Congress Debates New Tax Plan Targeting Corporate Profits | 0.39 | -0.01 |
| Bank of Japan Ends Negative Interest Rate Policy | 0.39 | -0.01 |
| Small Business Confidence Index Drops to Lowest Since 2020 | 0.39 | -0.01 |
| Global Supply Chain Disruptions Ease as Shipping Costs Decline | 0.40 | -0.00 |
| Baltic Dry Index Plunges Signaling Weakening Global Trade | 0.38 | -0.02 |
| Durable Goods Orders Rise 1.4%, Signaling Business Investment | 0.36 | -0.04 |
| US Manufacturing ISM Index Unexpectedly Expands to 51.2 | 0.32 | -0.08 |
| Federal Minimum Wage Debate Heats Up in Senate | 0.30 | -0.10 |
| Oil Prices Surge After OPEC Announces Production Cuts | 0.26 | -0.14 |

**Observation:** 5 of 9 are within 0.02 of threshold. The reference sentences don't cover these economic topics well enough.

---

## Optimization Axes

### Axis 1: Reference Sentences
Add new sentences targeting the missed topic gaps:
- Oil/energy/commodity prices and OPEC
- Business confidence and sentiment indices
- Minimum wage and labor policy
- Supply chain and shipping logistics
- Manufacturing indices (ISM, PMI, durable goods)
- International trade indicators (Baltic Dry)
- Foreign central bank policy (BOJ, ECB, PBOC)
- Tax policy and fiscal legislation

### Axis 2: Threshold
Grid search thresholds from 0.25 to 0.50 (step 0.01) to find optimal balance between precision and recall.

### Axis 3: Scoring Strategy
- Current: **max** similarity (best single reference match)
- Try: **top-k mean** (average of top 3 reference matches) — may be more robust
- Try: **weighted max** (max score × coverage bonus if multiple refs match above a floor)

### Axis 4: Embedding Model
Compare models on same data:
- `all-MiniLM-L6-v2` (current, 80MB, 384-dim)
- `all-mpnet-base-v2` (higher quality, 420MB, 768-dim)
- `BAAI/bge-small-en-v1.5` (strong, 130MB, 384-dim)

---

## Files to Create

| File | Purpose |
|---|---|
| `eco_ref_sentences_v2.txt` | Expanded reference sentences (original 12 + new ones for missed topics) |
| `tune_threshold.py` | Grid search threshold on current + v2 refs, output precision/recall/F1 curve |
| `tune_scoring.py` | Compare max vs top-k-mean vs weighted scoring strategies |
| `tune_model.py` | Compare embedding models on same data + refs |
| `tune_all.py` | Full grid search: model × refs × threshold × scoring → find best combo |
| `results.md` | Auto-generated results from best run |

All scripts read `sampledata.yaml` and `labels.yaml` from `../poc-eco-classify/`.

---

## Step 1: Expanded Reference Sentences (`eco_ref_sentences_v2.txt`)

Original 12 sentences + 8 new ones covering missed topics:

```
# Original 12
Economic growth and GDP quarterly report shows expansion or contraction
Federal Reserve interest rate decision and monetary policy announcement
Inflation rate and consumer price index CPI rising or falling
Unemployment rate and weekly jobless claims labor market report
International trade deficit and tariff policy changes
Government fiscal policy budget deficit and spending plans
Consumer spending and retail sales data for the quarter
Housing market mortgage rates and new home construction starts
Manufacturing output and factory orders industrial production
Wage growth and personal income changes affecting workers
Central bank policy decisions affecting the global economy
Recession fears and economic slowdown indicators

# New: cover missed topics
Oil and energy commodity prices OPEC production decisions affecting economy
Business confidence sentiment index and small business economic outlook
Minimum wage labor policy debate and workforce economic regulation
Supply chain disruptions shipping costs and logistics economic impact
ISM manufacturing index PMI durable goods orders economic signals
Baltic Dry Index global trade volume and shipping demand indicator
Foreign central bank policy Bank of Japan ECB interest rate changes
Tax reform corporate tax policy and fiscal legislation economic impact
```

---

## Step 2: Threshold Grid Search (`tune_threshold.py`)

For each reference set (v1, v2):
1. Compute scores for all 60 articles
2. Sweep threshold from 0.25 to 0.50 (step 0.01)
3. At each threshold compute accuracy, precision, recall, F1
4. Print table + highlight best F1 and best accuracy
5. Show the precision-recall tradeoff

Output:
```
Reference set: eco_ref_sentences.txt (12 refs)
Threshold  Accuracy  Precision  Recall  F1
0.25       0.XX      0.XX       0.XX    0.XX
0.26       ...
...
0.50       ...
Best F1: threshold=X.XX, F1=X.XX
Best Accuracy: threshold=X.XX, accuracy=X.XX

Reference set: eco_ref_sentences_v2.txt (20 refs)
...
```

---

## Step 3: Scoring Strategy Comparison (`tune_scoring.py`)

For each scoring strategy, sweep thresholds and report best F1:

1. **max** — `max(similarities)` (current)
2. **top3_mean** — `mean(top 3 similarities)`
3. **mean_all** — `mean(all similarities)`
4. **weighted_max** — `max_sim * (1 + 0.1 * count_above_floor)` where floor = 0.25

Output: best threshold + metrics for each strategy × each ref set.

---

## Step 4: Model Comparison (`tune_model.py`)

For each model, using best ref set + best scoring from Steps 2-3:
1. `all-MiniLM-L6-v2` (current)
2. `all-mpnet-base-v2`
3. `BAAI/bge-small-en-v1.5`

Report: accuracy, F1, speed, model size for each.

---

## Step 5: Full Grid Search (`tune_all.py`)

Combine all axes:
- 3 models × 2 ref sets × 4 scoring strategies × 26 thresholds = 624 combos
- Report top 10 combos by F1, then by accuracy
- Save full results to `results.md`

Output:
```
TOP 10 BY F1
Rank  Model         Refs  Scoring     Threshold  Acc   Prec  Rec   F1
1     mpnet-base    v2    top3_mean   0.33       0.XX  0.XX  0.XX  0.XX
2     ...
...

TOP 10 BY ACCURACY
...

RECOMMENDED CONFIG
  Model:     ...
  Refs:      ...
  Scoring:   ...
  Threshold: ...
  Accuracy:  X.XX
  F1:        X.XX
```

---

## Dependencies

Uses same venv from `../poc-eco-classify/`. No new deps needed (sentence-transformers, numpy, sklearn, pyyaml already installed).

If `BAAI/bge-small-en-v1.5` or `all-mpnet-base-v2` need downloading, they auto-download on first use.

---

## Run

```bash
cd embedding-tuning

# Step by step
../poc-eco-classify/.venv/bin/python tune_threshold.py      # ~10s
../poc-eco-classify/.venv/bin/python tune_scoring.py        # ~10s
../poc-eco-classify/.venv/bin/python tune_model.py          # ~30s (downloads models)
../poc-eco-classify/.venv/bin/python tune_all.py            # ~2min (full grid)
```

---

## Execution Order

1. Create `eco_ref_sentences_v2.txt` (expanded refs)
2. Create `tune_threshold.py`
3. Run threshold tuning → identify best threshold for v1 and v2 refs
4. Create `tune_scoring.py`
5. Run scoring tuning → identify best scoring strategy
6. Create `tune_model.py`
7. Run model comparison → identify best model
8. Create `tune_all.py`
9. Run full grid search → get final recommended config
10. Generate `results.md`
