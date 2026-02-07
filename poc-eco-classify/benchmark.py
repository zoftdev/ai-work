"""
Benchmark: compare sentence embedding vs zero-shot classification
for economic news. Runs each method in a separate subprocess so
memory is fully released between runs (avoids OOM on 16GB Macs).
"""
import json
import subprocess
import sys
from pathlib import Path

import yaml
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def load_sampledata(path: str = "sampledata.yaml") -> tuple[list[str], list[str]]:
    """Returns (titles, answer_labels)."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    titles = [item["title"] for item in data]
    answers = [item["answer"] for item in data]
    return titles, answers


def load_target(path: str = "labels.yaml") -> str:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data["target"]


def run_method(script: str, data_file: str = "sampledata.yaml") -> dict:
    """Run a method script as a subprocess and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, script, data_file],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent),
    )
    if result.returncode != 0:
        print(f"\n  ERROR running {script} (exit code {result.returncode})")
        if result.stderr:
            for line in result.stderr.strip().splitlines()[-10:]:
                print(f"    {line}")
        return None
    return json.loads(result.stdout.strip())


def print_method_results(name, y_true, predictions, elapsed, n, misclassified_info):
    acc = accuracy_score(y_true, predictions)
    prec = precision_score(y_true, predictions, zero_division=0)
    rec = recall_score(y_true, predictions, zero_division=0)
    f1 = f1_score(y_true, predictions, zero_division=0)

    print(f"{name}")
    print(f"  Accuracy:  {acc:.2f}")
    print(f"  Precision: {prec:.2f}")
    print(f"  Recall:    {rec:.2f}")
    print(f"  F1 Score:  {f1:.2f}")
    print(f"  Time:      {elapsed:.2f}s ({elapsed / n:.3f}s per article)")

    if misclassified_info:
        print("  Misclassified:")
        for item in misclassified_info:
            print(f"    {item}")
    else:
        print("  Misclassified: (none)")
    print()

    return acc, prec, rec, f1


def main() -> None:
    titles, answers = load_sampledata()
    target = load_target()
    y_true = [a == target for a in answers]
    n = len(titles)
    n_economic = sum(y_true)
    n_non = n - n_economic

    print("=" * 60)
    print("BENCHMARK: Economic News Classification")
    print("=" * 60)
    print(f"Sample size: {n} articles ({n_economic} economic, {n_non} non-economic)")
    print(f"(Each method runs in a separate process to avoid OOM)\n")

    # --- Method 1: Embedding (subprocess) ---
    print("Running embedding method (subprocess)...")
    emb_result = run_method("method_embedding.py")

    acc_emb = prec_emb = rec_emb = f1_emb = time_emb = None
    if emb_result:
        pred_emb = emb_result["predictions"]
        scores_emb = emb_result["scores"]
        time_emb = emb_result["elapsed"]

        mis_emb = []
        for i in range(n):
            if pred_emb[i] != y_true[i]:
                kind = "FP" if pred_emb[i] else "FN"
                mis_emb.append(f'[{kind}] "{titles[i]}" (score: {scores_emb[i]:.2f}, actual: {answers[i]})')

        acc_emb, prec_emb, rec_emb, f1_emb = print_method_results(
            "METHOD 1: Sentence Embeddings (all-MiniLM-L6-v2)",
            y_true, pred_emb, time_emb, n, mis_emb,
        )
    else:
        print("  Skipped (failed to run)\n")

    # --- Method 2: Zero-shot (subprocess) ---
    print("Running zero-shot method (subprocess)...")
    zs_result = run_method("method_zeroshot.py")

    acc_zs = prec_zs = rec_zs = f1_zs = time_zs = None
    if zs_result:
        pred_zs = zs_result["predictions"]
        details_zs = zs_result["details"]
        time_zs = zs_result["elapsed"]

        mis_zs = []
        for i in range(n):
            if pred_zs[i] != y_true[i]:
                kind = "FP" if pred_zs[i] else "FN"
                d = details_zs[i]
                mis_zs.append(f'[{kind}] "{titles[i]}" (predicted: {d["top_label"]} {d["top_score"]:.2f}, actual: {answers[i]})')

        acc_zs, prec_zs, rec_zs, f1_zs = print_method_results(
            "METHOD 2: Zero-Shot Classification (bart-large-mnli)",
            y_true, pred_zs, time_zs, n, mis_zs,
        )
    else:
        print("  Skipped (failed to run)\n")

    # --- Comparison ---
    if acc_emb is not None and acc_zs is not None:
        print("=" * 60)
        print("COMPARISON")
        print("=" * 60)
        print(f"{'':14} {'Embedding':>12} {'Zero-Shot':>12}")
        print(f"Accuracy      {acc_emb:>12.2f} {acc_zs:>12.2f}")
        print(f"Precision     {prec_emb:>12.2f} {prec_zs:>12.2f}")
        print(f"Recall        {rec_emb:>12.2f} {rec_zs:>12.2f}")
        print(f"F1            {f1_emb:>12.2f} {f1_zs:>12.2f}")
        print(f"Speed         {time_emb:>11.2f}s {time_zs:>11.2f}s")
        print(f"Speed/article {time_emb/n:>11.3f}s {time_zs/n:>11.3f}s")
        print("Model size    ~80MB        ~1.6GB")
        print("=" * 60)
    elif acc_emb is not None:
        print("=" * 60)
        print("Only embedding method completed. Zero-shot failed (likely OOM).")
        print("Try closing other apps and re-running, or use a smaller model.")
        print("=" * 60)


if __name__ == "__main__":
    main()
