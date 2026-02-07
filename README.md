# AI Work

AI-assisted work projects and automation scripts.

## Projects

### [googlenews-fetch-news](./googlenews-fetch-news/)
Fetch Google News article metadata from whitelisted publishers. Stage 1: metadata only; output in YAML. Content fetch and summarization are external.

**Quick Start:**
```bash
cd googlenews-fetch-news
uv sync
./fetch.sh
```

### [google-news-check](./google-news-check/)
ETF news publisher analysis tool. Fetches and analyzes Google News articles to identify publishers worth following based on coverage patterns.

**Quick Start:**
```bash
cd google-news-check
uv venv
uv pip install -r requirements.txt
.venv/bin/python run_publisher_analysis.py
```

See [google-news-check/QUICKSTART.md](./google-news-check/QUICKSTART.md) for details.
