# POC: Economic News Classification Benchmark

## Goal

Compare two NLP approaches for classifying news articles as "economic" or not:

1. **Sentence Embeddings** — `sentence-transformers` with cosine similarity
2. **Zero-Shot Classification** — `transformers` pipeline with `facebook/bart-large-mnli`

Benchmark on **correctness** (accuracy, precision, recall, F1) and **speed** (time per article, total batch time).

---

## Files to Create

| File | Purpose |
|---|---|
| `sampledata.yaml` | News headlines with ground truth answers (60 items, each has `title` + `answer` category) |
| `labels.yaml` | Category definitions for zero-shot classifier. Defines `target` category and all candidate `categories` with descriptions. |
| `eco_ref_sentences.txt` | Economic reference sentences for embedding method, one per line |
| `method_embedding.py` | Sentence embedding classifier (reads `eco_ref_sentences.txt`) |
| `method_zeroshot.py` | Zero-shot classification classifier (reads `labels.yaml` for candidate categories) |
| `benchmark.py` | Run both methods, compare correctness & speed, print report (reads `sampledata.yaml` for articles + ground truth) |
| `requirements.txt` | Dependencies (includes `pyyaml`) |

---

## Step 1: Data Files

### sampledata.yaml

60 labeled articles. Each entry has `title` (headline text) and `answer` (ground truth category from `labels.yaml` categories).

```yaml
- title: "US GDP Grows 3.2% in Q4, Beating Expectations"
  answer: economic
- title: "Apple Launches New iPhone 17 Pro with Advanced AI Features"
  answer: technology
```

Ground truth distribution:
- 30 x `economic`
- 30 x non-economic (spread across: `technology`, `finance`, `science`, `sports`, `entertainment`, `health`, `disaster`, `politics`)

### labels.yaml

Defines classification categories for the zero-shot method. Structure:

```yaml
target: economic            # which category we want to detect

categories:                 # all candidate labels with descriptions
  economic: "economic news about GDP, inflation, interest rates..."
  finance: "financial markets news about stocks, ETFs, earnings..."
  technology: "technology news about product launches, software..."
  science: "science news about research, discoveries..."
  sports: "sports news about games, tournaments..."
  entertainment: "entertainment news about movies, music..."
  health: "health and medical news..."
  disaster: "natural disaster and extreme weather news..."
  politics: "political news not related to economy..."
```

The zero-shot model scores each article against **all 9 categories**. An article is classified as economic if `economic` is the top-scoring category.

This also gives us a bonus: we see **what category** the model thinks each non-economic article belongs to (tech? finance? sports?).

---

## Step 2: Economic Reference Sentences (`eco_ref_sentences.txt`)

Used by the embedding method as "what economic news sounds like". One sentence per line.

```
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
```

---

## Step 3: Sentence Embedding Method (`method_embedding.py`)

- Model: `all-MiniLM-L6-v2` (small, fast, ~80MB)
- Load reference sentences from `eco_ref_sentences.txt`
- Encode all references once at startup
- For each article: encode → compute cosine similarity against all reference vectors → take **max** score
- Classify as economic if max score > threshold (default 0.40)
- Return: list of predictions + time taken

Interface:
```python
def classify(articles: list[str], ref_file: str = "eco_ref_sentences.txt", threshold: float = 0.40) -> tuple[list[bool], float]:
    """Returns (predictions, elapsed_seconds)"""
```

Note: Model loading time is excluded from benchmark timing. Only inference time is measured.

---

## Step 4: Zero-Shot Classification Method (`method_zeroshot.py`)

- Model: `facebook/bart-large-mnli`
- Pipeline: `zero-shot-classification`
- Load candidate categories from `labels.yaml` (category descriptions as labels)
- Load target category name from `labels.yaml` (`target` field)
- Classify as economic if the target category has the highest score among all candidates
- Return: list of predictions + scores + time taken

Interface:
```python
def classify(articles: list[str], labels_file: str = "labels.yaml") -> tuple[list[bool], list[dict], float]:
    """Returns (predictions, details, elapsed_seconds)

    details: list of {top_label: str, top_score: float, target_score: float} per article
    """
```

Note: Model loading time is excluded from benchmark timing. Only inference time is measured.

---

## Step 5: Benchmark Runner (`benchmark.py`)

1. Load `sampledata.yaml` → extract articles (titles) and ground truth (answer == target category from `labels.yaml`)
2. Run **Method 1** (embedding) → collect predictions + time
3. Run **Method 2** (zero-shot) → collect predictions + time
4. Compute metrics for each using sklearn:
   - Accuracy, Precision, Recall, F1
   - Total time, time per article
5. Show **misclassified articles** for each method with ground truth category
6. Print comparison table

Expected output:
```
============================================================
BENCHMARK: Economic News Classification
============================================================
Sample size: 60 articles (30 economic, 30 non-economic)

METHOD 1: Sentence Embeddings (all-MiniLM-L6-v2)
  Accuracy:  0.XX
  Precision: 0.XX
  Recall:    0.XX
  F1 Score:  0.XX
  Time:      X.XXs (X.XXXs per article)

  Misclassified:
    [FP] "Article title..." (score: 0.XX, actual: finance)
    [FN] "Article title..." (score: 0.XX, actual: economic)

METHOD 2: Zero-Shot Classification (bart-large-mnli)
  Accuracy:  0.XX
  Precision: 0.XX
  Recall:    0.XX
  F1 Score:  0.XX
  Time:      X.XXs (X.XXXs per article)

  Misclassified:
    [FP] "Article title..." (predicted: economic 0.XX, actual: finance)
    [FN] "Article title..." (predicted: finance 0.XX, actual: economic)

============================================================
COMPARISON
============================================================
              Embedding    Zero-Shot
Accuracy      0.XX         0.XX
Precision     0.XX         0.XX
Recall        0.XX         0.XX
F1            0.XX         0.XX
Speed         X.XXs        X.XXs
Speed/article X.XXXs       X.XXXs
Model size    ~80MB        ~1.6GB
============================================================
```

---

## Step 6: Dependencies (`requirements.txt`)

```
sentence-transformers
transformers
torch
scikit-learn
pyyaml
```

---

## Setup & Run

```bash
cd poc-eco-classify
uv venv
uv pip install -r requirements.txt
.venv/bin/python benchmark.py
```

---

## Execution Order

1. Create `sampledata.yaml` (60 articles with ground truth) ✅
2. Create `labels.yaml` (9 category definitions) ✅
3. Create `eco_ref_sentences.txt` (12 reference sentences) ✅
4. Create `requirements.txt` ✅
5. Setup venv + install deps ✅
6. Create `method_embedding.py` ✅
7. Create `method_zeroshot.py` (reads `labels.yaml`) ✅
8. Create `benchmark.py` (reads `sampledata.yaml` for articles + ground truth) ✅
9. Run benchmark, review results ✅

**Note:** Full benchmark loads both models (~80MB + ~1.6GB). If the process is killed (e.g. exit 138), try `python benchmark.py --embedding-only` to run only the embedding method.
