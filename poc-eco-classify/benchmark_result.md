# Benchmark Result: Economic News Classification

Run date: 2026-02-07
Machine: macOS ARM64, 16GB RAM

## Comparison

| Metric | Embedding | Zero-Shot |
|---|---|---|
| Accuracy | **0.85** | 0.60 |
| Precision | **1.00** | 0.56 |
| Recall | 0.70 | **1.00** |
| F1 | **0.82** | 0.71 |
| Speed | **0.10s** | 117.80s |
| Speed/article | **0.002s** | 1.963s |
| Model size | ~80MB | ~350MB |

Sample size: 60 articles (30 economic, 30 non-economic)

## Method 1: Sentence Embeddings (all-MiniLM-L6-v2)

- Threshold: 0.40
- Reference sentences: 12 (from `eco_ref_sentences.txt`)
- **Zero false positives** — never misclassified non-economic as economic
- 9 false negatives — missed indirect economic articles

### Misclassified (all False Negatives)

| Title | Score | Actual |
|---|---|---|
| Congress Debates New Tax Plan Targeting Corporate Profits | 0.39 | economic |
| Oil Prices Surge After OPEC Announces Production Cuts | 0.26 | economic |
| Bank of Japan Ends Negative Interest Rate Policy | 0.39 | economic |
| Small Business Confidence Index Drops to Lowest Since 2020 | 0.39 | economic |
| Durable Goods Orders Rise 1.4%, Signaling Business Investment | 0.36 | economic |
| Global Supply Chain Disruptions Ease as Shipping Costs Decline | 0.40 | economic |
| Federal Minimum Wage Debate Heats Up in Senate | 0.30 | economic |
| US Manufacturing ISM Index Unexpectedly Expands to 51.2 | 0.32 | economic |
| Baltic Dry Index Plunges Signaling Weakening Global Trade | 0.38 | economic |

## Method 2: Zero-Shot Classification (DeBERTa-v3-base-mnli-fever-anli)

- Originally planned `facebook/bart-large-mnli` (~1.6GB) but OOM on 16GB Mac (exit code -10)
- Switched to `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` (~350MB)
- **Caught all 30 economic articles** (recall 1.00)
- 24 false positives — classified most non-economic articles as economic too

### Misclassified (all False Positives)

| Title | Predicted Score | Actual |
|---|---|---|
| SpaceX Successfully Lands Starship After Orbital Flight | 0.37 | science |
| Golden State Warriors Win NBA Championship in Game 7 | 0.32 | sports |
| Netflix Adds 13 Million Subscribers in Record Quarter | 0.42 | entertainment |
| New Study Links Ultra-Processed Food to Heart Disease Risk | 0.25 | health |
| NASA's James Webb Telescope Discovers New Exoplanet | 0.33 | science |
| Taylor Swift Announces New World Tour Dates for 2026 | 0.25 | entertainment |
| Meta Unveils Next-Generation VR Headset at Connect Conference | 0.35 | technology |
| Severe Thunderstorms Expected Across Midwest This Weekend | 0.34 | disaster |
| Olympic Committee Confirms New Sports for 2028 Los Angeles Games | 0.41 | sports |
| Marvel Studios Announces Phase 7 Movie Lineup | 0.55 | entertainment |
| Scientists Achieve Breakthrough in Quantum Computing | 0.39 | science |
| Wildfire in California Forces Evacuation of 50,000 Residents | 0.31 | disaster |
| Tesla Recalls 500,000 Vehicles Over Autopilot Software Issue | 0.36 | technology |
| Pfizer Announces New Cancer Treatment Shows Promise in Trials | 0.34 | health |
| AI-Generated Art Wins First Prize at International Competition | 0.44 | technology |
| Samsung Launches Galaxy S26 with Foldable Display | 0.33 | technology |
| Tour de France 2026 Route Revealed with New Mountain Stages | 0.34 | sports |
| Disney Plus Surpasses 200 Million Global Subscribers | 0.35 | entertainment |
| Researchers Develop New Plastic-Eating Enzyme | 0.31 | science |
| Google DeepMind AI Solves New Mathematical Theorem | 0.35 | science |
| NVIDIA Stock Jumps 15% After Blowout Earnings Report | 0.31 | finance |
| Historic Flooding in Brazil Displaces Thousands | 0.36 | disaster |
| SpaceX Starlink Reaches 5 Million Users Worldwide | 0.34 | technology |
| New York City Bans Gas Stoves in All New Construction | 0.32 | politics |

## Verdict

**Sentence Embedding is the recommended approach.**

| | Embedding | Zero-Shot |
|---|---|---|
| Accuracy | Better (0.85) | Poor (0.60) |
| False positives | None | 24 out of 30 non-economic |
| Speed | 1000x faster | ~2 min for 60 articles |
| RAM | Fits easily | OOM with bart-large on 16GB |
| Tunability | Add reference sentences | Rewrite label descriptions |

## Next Steps

To improve the embedding method's recall (currently misses 9/30 economic articles):

1. **Lower threshold** from 0.40 to 0.35 — would catch 4 more (scores 0.36-0.39) but may add false positives
2. **Add reference sentences** to `eco_ref_sentences.txt` for missing topics:
   - Oil/energy prices and OPEC decisions
   - Business confidence and sentiment indices
   - Minimum wage and labor policy debates
   - Supply chain and shipping/logistics
   - ISM manufacturing and durable goods orders
   - International trade indices (Baltic Dry)
