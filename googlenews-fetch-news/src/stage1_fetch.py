#!/usr/bin/env python3
"""
Stage 1: Fetch article metadata from Google News.
- Reads publisher whitelist and search queries from config files.
- Fetches articles (last 1 day), filters by whitelist, deduplicates by URL.
- Outputs data/articles_YYYYMMDD_HHMMSS.yaml (timestamped) and appends new URLs to data/processed_urls.txt.
"""

from gnews import GNews
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import yaml


def project_root() -> Path:
    """Project root (directory containing publisher_whitelist.txt)."""
    return Path(__file__).resolve().parent.parent


def load_lines(path: Path, strip_empty: bool = True) -> list[str]:
    """Load non-empty lines from a text file."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines()]
    return [l for l in lines if l] if strip_empty else lines


def load_whitelist(root: Path) -> set[str]:
    """Load publisher whitelist (exact names, case-sensitive)."""
    path = root / "publisher_whitelist.txt"
    return set(load_lines(path))


def load_search_queries(root: Path) -> list[str]:
    """Load search terms and combine with OR."""
    path = root / "search_queries.txt"
    return load_lines(path)


def combined_query(queries: list[str]) -> str:
    """Combine search terms with OR."""
    return " OR ".join(queries) if queries else "ETF"


def get_publisher(article: dict) -> str:
    """Extract publisher name from GNews article (publisher.title or source)."""
    pub = article.get("publisher")
    if isinstance(pub, dict) and pub.get("title"):
        return pub["title"].strip()
    if isinstance(article.get("source"), str):
        return article["source"].strip()
    return ""


def parse_published_date(date_str: str) -> str:
    """Parse GNews date and return YAML-friendly string (YYYY-MM-DD HH:MM:SS)."""
    if not date_str:
        return ""
    try:
        # Format: "Fri, 06 Feb 2026 18:45:04 GMT"
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return date_str


def load_processed_urls(data_dir: Path) -> set[str]:
    """Load set of already-processed URLs."""
    path = data_dir / "processed_urls.txt"
    return set(load_lines(path))


def append_processed_urls(data_dir: Path, urls: list[str]) -> None:
    """Append new URLs to processed_urls.txt."""
    path = data_dir / "processed_urls.txt"
    with path.open("a", encoding="utf-8") as f:
        for u in urls:
            f.write(u + "\n")


def resolve_data_dir(root: Path, cli_arg: str | None, config_path: Path) -> Path:
    """Resolve data directory: CLI > config.yaml > default 'data' (relative to root)."""
    if cli_arg is not None:
        p = Path(cli_arg)
        return p.resolve() if not p.is_absolute() else p
    if config_path.exists():
        with config_path.open(encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        if cfg.get("data_dir"):
            p = Path(cfg["data_dir"])
            return (root / p).resolve() if not p.is_absolute() else p.resolve()
    return (root / "data").resolve()


def run() -> None:
    root = project_root()
    parser = argparse.ArgumentParser(description="Stage 1: Fetch article metadata from Google News.")
    parser.add_argument("--data-dir", type=str, default=None, help="Output directory for YAML and processed_urls.txt")
    args = parser.parse_args()

    data_dir = resolve_data_dir(root, args.data_dir, root / "config.yaml")
    data_dir.mkdir(parents=True, exist_ok=True)

    whitelist = load_whitelist(root)
    if not whitelist:
        print("No publishers in publisher_whitelist.txt. Add at least one.")
        return

    queries = load_search_queries(root)
    query_str = combined_query(queries)
    print(f"Query: {query_str}")
    print(f"Publishers: {sorted(whitelist)}")

    processed = load_processed_urls(data_dir)

    gn = GNews(
        language="en",
        country="US",
        max_results=100,
        start_date=(datetime.now() - timedelta(days=1)).date(),
        end_date=datetime.now().date(),
    )
    raw = gn.get_news(query_str)
    if not raw:
        print("No articles returned from Google News.")
        # Still write YAML with empty articles for consistency
        raw = []

    seen_urls = set()
    articles_out = []
    new_urls = []

    for article in raw:
        url = (article.get("url") or "").strip()
        if not url or url in seen_urls:
            continue
        publisher = get_publisher(article)
        if publisher not in whitelist:
            continue
        if url in processed:
            continue
        seen_urls.add(url)
        new_urls.append(url)
        articles_out.append({
            "title": (article.get("title") or "").strip(),
            "publisher": publisher,
            "url": url,
            "published": parse_published_date(article.get("published date", "")),
            "description": (article.get("description") or "").strip(),
        })

    payload = {
        "fetched_at": datetime.now().isoformat(),
        "query": query_str,
        "publishers_filter": sorted(whitelist),
        "articles": articles_out,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = data_dir / f"articles_{timestamp}.yaml"
    with out_path.open("w", encoding="utf-8") as f:
        yaml.dump(payload, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if new_urls:
        append_processed_urls(data_dir, new_urls)

    print(f"Fetched {len(raw)} raw; after whitelist + dedup: {len(articles_out)} new articles.")
    print(f"Written: {out_path}")
    if new_urls:
        print(f"Appended {len(new_urls)} URLs to processed_urls.txt.")


if __name__ == "__main__":
    run()
