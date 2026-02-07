"""
Zero-shot classifier for economic news.
Uses facebook/bart-large-mnli; classifies as economic if target category
has the highest score among all candidates from labels.yaml.
"""
from pathlib import Path

import yaml
from transformers import pipeline


def _load_labels(labels_file: str) -> tuple[str, list[str]]:
    path = Path(labels_file)
    if not path.exists():
        raise FileNotFoundError(f"Labels file not found: {labels_file}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    target = data["target"]
    categories = data["categories"]
    # Labels for the pipeline: list of "category: description"
    label_list = [f"{k}: {v}" for k, v in categories.items()]
    return target, label_list


def classify(
    articles: list[str],
    labels_file: str = "labels.yaml",
) -> tuple[list[bool], list[dict], float]:
    """
    Returns (predictions, details, elapsed_seconds).
    predictions[i] is True if article i is classified as economic (target wins).
    details[i] = {top_label: str, top_score: float, target_score: float}
    Only inference time is measured (model load excluded).
    """
    target, label_list = _load_labels(labels_file)
    pipe = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=-1,
    )

    import time
    t0 = time.perf_counter()
    predictions = []
    details = []
    for text in articles:
        out = pipe(text, label_list, multi_label=False)
        scores = dict(zip(out["labels"], out["scores"]))
        top_label_full = out["labels"][0]
        top_score = float(out["scores"][0])
        target_score = 0.0
        for k, v in scores.items():
            if k.startswith(target + ":") or k == target:
                target_score = float(v)
                break
        top_label = top_label_full.split(":")[0].strip() if ":" in top_label_full else top_label_full
        is_economic = top_label_full.startswith(target + ":") or top_label_full == target
        predictions.append(is_economic)
        details.append({
            "top_label": top_label,
            "top_score": top_score,
            "target_score": target_score,
        })
    elapsed = time.perf_counter() - t0
    return predictions, details, elapsed


if __name__ == "__main__":
    import json
    import sys

    data_file = sys.argv[1] if len(sys.argv) > 1 else "sampledata.yaml"
    data = yaml.safe_load(Path(data_file).read_text(encoding="utf-8"))
    titles = [item["title"] for item in data]

    preds, details, elapsed = classify(titles)
    json.dump({"predictions": preds, "details": details, "elapsed": elapsed}, sys.stdout)
    sys.stdout.write("\n")
