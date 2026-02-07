# googlenews-fetch-news

Fetch Google News article metadata from whitelisted publishers. Stage 1 only: metadata fetch; full content and summarization are handled elsewhere.

## Requirements

- [UV](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.11+

## Setup

```bash
cd googlenews-fetch-news
uv sync
```

## Configuration

- **publisher_whitelist.txt** — One publisher per line (exact names as shown in Google News, e.g. `The Motley Fool`, `ETF.com`).
- **search_queries.txt** — One search term per line. Terms are combined with OR (e.g. `ETF`, `THD`, `GLD` → query `ETF OR THD OR GLD`).
- **data directory** — Where YAML and `processed_urls.txt` are written. Priority: `--data-dir` CLI arg → `data_dir` in **config.yaml** (copy from `config.yaml.example`) → default `data/`.

## Usage

```bash
./fetch.sh
```

Or with a custom data directory:

```bash
./fetch.sh --data-dir /path/to/output
uv run python src/stage1_fetch.py --data-dir /path/to/output
```

- Fetches from Google News (last 1 day).
- Keeps only articles from whitelisted publishers.
- Skips URLs already in `data/processed_urls.txt`.
- Writes metadata to **data/articles_YYYYMMDD_HHMMSS.yaml** (one timestamped file per run).
- Appends new URLs to **data/processed_urls.txt**.

Safe to run multiple times per day; duplicates are skipped. Each run creates a new YAML file (no overwrite).

## Output (Stage 1)

**data/articles_YYYYMMDD_HHMMSS.yaml** (YAML, one file per run):

```yaml
fetched_at: "2026-02-07T12:00:00"
query: "ETF OR THD OR GLD OR bitcoin ETF"
publishers_filter:
  - "ETF Trends"
  - "The Motley Fool"
  - ...
articles:
  - title: "Article title..."
    publisher: "The Motley Fool"
    url: "https://..."
    published: "2026-02-07 10:30:00"
    description: "Article snippet..."
```

Full content fetching and summarization are done by an external application; this repo only produces the metadata above.
