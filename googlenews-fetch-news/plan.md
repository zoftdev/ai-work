# Plan: Create Google News Fetch App with Publisher Whitelist

## THIS PHASE: Stage 1 Only (Metadata Fetch)

**What we're building NOW:**
- ✓ UV Python project structure
- ✓ Stage 1: Fetch article metadata from Google News
- ✓ Publisher whitelist filtering
- ✓ Search query configuration (combined with OR)
- ✓ Deduplication tracking (processed_urls.txt)
- ✓ Output in YAML format

**What we're NOT building yet:**
- ✗ Stage 2: Full content fetching (future phase)
- ✗ Summarization (will be external application)

## Context

The user wants a new Python application under `ai-work/googlenews-fetch-news` that:
1. Fetches Google News articles from whitelisted publishers
2. Uses a two-stage process:
   - **Stage 1**: Fetch article metadata from Google News RSS
   - **Stage 2**: Access actual article URLs and generate content summaries
3. Uses UV for project management
4. Includes a shell script for easy execution

This differs from the existing `google-news-check` which analyzes all ETF publishers. This new app focuses on fetching and summarizing content from pre-selected publishers only.

## Approach

### Project Structure
```
ai-work/
├── google-news-check/              (existing)
└── googlenews-fetch-news/          (new)
    ├── pyproject.toml              (UV project config)
    ├── README.md                   (Documentation)
    ├── config.yaml.example         (Config template - committed)
    ├── config.yaml                 (Local config - git-ignored)
    ├── fetch.sh                    (Shell script to run Stage 1)
    ├── publisher_whitelist.txt     (List of allowed publishers)
    ├── search_queries.txt          (Search terms - combined with OR)
    ├── data/                       (Output directory - configurable)
    │   ├── articles_YYYYMMDD_HHMMSS.yaml  (Stage 1: timestamped per run)
    │   └── processed_urls.txt      (Tracking processed articles)
    └── src/
        ├── __init__.py
        └── stage1_fetch.py         (Fetch from Google News)
```

**Note**: Stage 2 (fetch_content.py) will be implemented in a future phase.

### Implementation Plan

#### 1. Initialize UV Project
- Create new directory: `ai-work/googlenews-fetch-news`
- Run `uv init` to create project structure
- Add dependencies: `gnews`, `pyyaml` (for Stage 1 only)

#### 2. Create Configuration Files
- `publisher_whitelist.txt` - One publisher per line
  - Format: Exact publisher names from Google News (e.g., "The Motley Fool", "ETF.com")
- `search_queries.txt` - One search term per line (combined with OR)
  - Format: Search terms like "THD", "GLD", "bitcoin ETF"
  - Will be combined as: "THD OR GLD OR bitcoin ETF"

#### 3. Stage 1: Fetch Article Metadata (THIS PHASE)
**File**: `src/stage1_fetch.py`

Features:
- Resolve data directory path (priority: `--data-dir` CLI arg > `config.yaml` > default `data/`)
- Read publisher whitelist from `publisher_whitelist.txt`
- Read search queries from `search_queries.txt`
- Combine queries with OR operator (e.g., "THD OR GLD OR bitcoin ETF")
- Fetch articles from Google News (last 1 day)
- Filter articles to only include whitelisted publishers
- Check `<data_dir>/processed_urls.txt` to skip already-fetched articles
- Save metadata to `data/articles_YYYYMMDD_HHMMSS.yaml` (timestamped per run, never overwrites):
  ```yaml
  fetched_at: "2026-02-07T12:00:00"
  query: "THD OR GLD OR bitcoin ETF"
  publishers_filter:
    - "Publisher 1"
    - "Publisher 2"
  articles:
    - title: "Article title..."
      publisher: "The Motley Fool"
      url: "https://..."
      published: "2026-02-07 10:30:00"
      description: "Article snippet..."
    - title: "Another article..."
      publisher: "ETF Trends"
      url: "https://..."
      published: "2026-02-07 09:15:00"
      description: "Another snippet..."
  ```
- Append new URLs to `data/processed_urls.txt`

#### 4. Stage 2: Fetch Full Content (FUTURE PHASE)
**File**: `src/stage2_fetch_content.py` *(not implemented yet)*

Will be implemented in a future phase:
- Read latest `data/articles_*.yaml` (or all timestamped files)
- Fetch full content from article URLs
- Extract main text, authors, publish date
- Save to `data/articles_full.yaml`
- Summarization will be handled by separate external application

#### 5. Shell Script
**File**: `fetch.sh`

```bash
#!/bin/bash
set -e  # Exit on error

echo "🔍 Fetching article metadata from Google News..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
uv run python src/stage1_fetch.py "$@"

echo ""
echo "✓ Complete! Results saved to data/ (timestamped YAML)"
echo ""
echo "Next: Run external application for content fetching & summarization"
```

#### 6. Configuration Files
- `config.yaml` - Runtime config (git-ignored, local to user)
  - `data_dir`: path to output directory (default: `data`)
- `config.yaml.example` - Template showing available settings (committed)
- `publisher_whitelist.txt` - Which publishers to include (one per line)
- `search_queries.txt` - Search terms to query (one per line, combined with OR)
- `<data_dir>/processed_urls.txt` - URLs already processed (auto-generated, prevents re-processing)

**Data path resolution (priority):**
1. `--data-dir` CLI argument (highest)
2. `data_dir` in `config.yaml`
3. Default: `data/` relative to project root (lowest)

**Deduplication Logic:**
- Before fetching full content, check if URL exists in `processed_urls.txt`
- Skip already-processed articles
- Append new URLs after successful processing
- Allows running fetch.sh multiple times per day without duplicate work

## Critical Files

### Existing (Reference)
- `/Users/thisadee_pre/play/ai-work/google-news-check/fetch_etf_news_multiday.py` - Existing fetch logic to adapt
- `/Users/thisadee_pre/play/ai-work/google-news-check/analyze_publishers.py` - Publisher handling patterns

### New Files to Create (THIS PHASE)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/pyproject.toml` (UV project file)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/config.yaml.example` (Config template - committed)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/fetch.sh` (Shell script)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/publisher_whitelist.txt` (Config)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/search_queries.txt` (Config)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/.gitignore` (Git ignore)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/README.md` (Documentation)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/src/__init__.py` (Python package marker)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/src/stage1_fetch.py` (Main script)
- `/Users/thisadee_pre/play/ai-work/googlenews-fetch-news/data/.gitkeep` (Directory marker)

### Files Auto-Generated (by script)
- `data/articles_YYYYMMDD_HHMMSS.yaml` (Stage 1 output, timestamped per run)
- `data/processed_urls.txt` (Deduplication tracking)

## Implementation Steps

1. **Create UV project**
   ```bash
   cd /Users/thisadee_pre/play/ai-work
   mkdir googlenews-fetch-news && cd googlenews-fetch-news
   uv init --name googlenews-fetch-news
   ```

2. **Add dependencies**
   ```bash
   uv add gnews pyyaml
   ```

3. **Create directory structure**
   ```bash
   mkdir -p src data
   touch src/__init__.py
   ```

4. **Create configuration files**

   `publisher_whitelist.txt`:
   ```
   ETF Trends
   Yahoo Finance
   The Motley Fool
   CoinDesk
   ETF Express
   ```

   `search_queries.txt`:
   ```
   ETF
   THD
   GLD
   bitcoin ETF
   ```

5. **Implement stage1_fetch.py** (THIS PHASE)
   - Parse `--data-dir` CLI arg via argparse
   - Load `config.yaml` if exists, read `data_dir`
   - Resolve data path: CLI arg > config.yaml > default `data/`
   - Load whitelist from `publisher_whitelist.txt`
   - Load search queries from `search_queries.txt`
   - Combine queries with OR: "ETF OR THD OR GLD OR bitcoin ETF"
   - Fetch from Google News using gnews (last 1 day)
   - Filter by publisher whitelist
   - Load processed_urls.txt (if exists) to skip duplicates
   - Save to `<data_dir>/articles_YYYYMMDD_HHMMSS.yaml` (timestamped, never overwrites)
   - Append new URLs to `<data_dir>/processed_urls.txt`

6. **Create fetch.sh** (THIS PHASE)
   - Make executable: `chmod +x fetch.sh`
   - Run Stage 1 only

7. **Create README.md** (THIS PHASE)
   - Usage instructions
   - Configuration guide
   - Data format documentation

8. **Create .gitignore** (THIS PHASE)
   - Ignore `data/*.yaml` (generated files)
   - Ignore `data/processed_urls.txt` (local tracking)
   - Ignore `config.yaml` (local config with user-specific paths)

9. **Update main ai-work README.md** (THIS PHASE)
   - Add googlenews-fetch-news to projects list

**Future Phase (NOT NOW)**:
- Implement `stage2_fetch_content.py` for full content fetching

## Reusable Components

From `google-news-check`:
- `fetch_etf_news_multiday.py` line 11-18: Date parsing function
- `fetch_etf_news_multiday.py` line 33-42: GNews initialization pattern
- Publisher filtering logic (adapt from analyze_publishers.py)

## Deduplication Strategy

**Problem**: Running fetch.sh multiple times per day shouldn't re-process same articles

**Solution**:
1. Maintain `data/processed_urls.txt` - one URL per line
2. Before Stage 2 processes an article, check if URL is in file
3. Only fetch full content for new URLs
4. Append successfully processed URLs to file

**Benefits**:
- Can run fetch.sh hourly/daily without waste
- Handles incremental updates efficiently
- Simple text file format (easy to inspect/edit)

## Verification

After implementation:
1. **Initial run**: `./fetch.sh`
   - Check `data/articles_YYYYMMDD_HHMMSS.yaml` is created
   - Verify YAML is valid and human-readable
   - Check only whitelisted publishers are included
   - Verify `data/processed_urls.txt` is created with fetched URLs

2. **Second run** (same day): `./fetch.sh` again
   - A new timestamped YAML file is created; previous file is untouched
   - Should skip already-fetched URLs (check processed_urls.txt)
   - Only new articles (if any) appear in the new file

3. **Different queries**: Edit `search_queries.txt`
   - Add/remove search terms
   - Run `./fetch.sh`
   - Check console output shows combined query with OR operator
   - Verify articles match the new query terms

4. **YAML format**: Inspect latest `data/articles_*.yaml`
   - Should be valid YAML (not JSON)
   - Human-readable with proper indentation
   - Contains expected fields: title, publisher, url, published, description

Success criteria (THIS PHASE):
- ✓ Only articles from whitelisted publishers are fetched
- ✓ Search queries are combined with OR operator
- ✓ Duplicate URLs are not re-fetched (deduplication works)
- ✓ Data is saved in YAML format (not JSON)
- ✓ YAML files are valid and human-readable
- ✓ Shell script runs Stage 1 without errors
- ✓ processed_urls.txt tracks all fetched articles

Future phases will add:
- Stage 2: Full content fetching
- External summarization application

## User Clarifications (Received)

1. **Search query**: ✓ Configurable as list in `search_queries.txt`, combined with OR
2. **Summary**: ✓ Will be handled by external application (not this app)
3. **Date range**: ✓ Fetch last 1 day only
4. **Deduplication**: ✓ Track processed URLs to avoid re-processing same content
