# ETF News Publisher Analysis

## Quick Start - What You Want

**Goal:** Review 3 days of ETF news and analyze which publishers you'd be interested in.

**Command:**
```bash
.venv/bin/python run_publisher_analysis.py
```

This will:
1. Fetch 3 days of ETF news articles
2. Analyze all publishers
3. Show recommendations by interest area
4. Save data locally for further analysis

---

## What This Does

This tool helps you:
- **Discover publishers** that cover ETF news you care about
- **Analyze coverage patterns** (who covers Bitcoin ETFs? Vanguard? Dividends?)
- **Get recommendations** for publishers based on your interests
- **Save all data locally** for your own analysis

---

## Files Explained

### Main Scripts (Use These)
- **`run_publisher_analysis.py`** - ONE-CLICK solution. Run this!
- **`fetch_etf_news_multiday.py`** - Fetch N days of articles
- **`analyze_publishers.py`** - Analyze publishers from saved data

### Data Files (Auto-generated)
- **`etf_news_3days.json`** - Raw article data (100+ articles)
- **`publisher_report.md`** - Human-readable analysis report

### Setup Files
- **`.venv/`** - Python virtual environment
- **`requirements.txt`** - Python dependencies

---

## How to Use

### Option 1: Quick Analysis (Default: 3 days)
```bash
.venv/bin/python run_publisher_analysis.py
```

### Option 2: Custom Number of Days
```bash
.venv/bin/python run_publisher_analysis.py 7
```

### Option 3: Just Fetch Data (No Analysis)
```bash
.venv/bin/python fetch_etf_news_multiday.py 3
```

### Option 4: Analyze Existing Data
```bash
.venv/bin/python analyze_publishers.py
```

---

## Example Output

You'll get:

### 1. Publisher Rankings
```
TOP PUBLISHERS BY VOLUME
1. ETF Trends          25 articles, 10 topics
2. Yahoo Finance       21 articles, 11 topics
3. The Motley Fool     18 articles, 11 topics
```

### 2. Specialization Analysis
```
Bitcoin/Crypto Specialists:
  - CoinDesk: 3 articles

Investment Advice:
  - The Motley Fool: 12 articles
  - Yahoo Finance: 11 articles
```

### 3. Publisher Profiles
```
ETF Trends (25 articles)
Topics: General (52%), Investment Advice (16%), International (12%)
Sample Headlines:
  • New Global Equities ETF Launch
  • Derivative Income Strategies
```

### 4. Recommendations
```
📊 For Comprehensive Coverage: ETF Trends, Yahoo Finance
🎯 For Investment Advice: The Motley Fool, Yahoo Finance
📈 For Market Data: Morningstar, CoinDesk
🆕 For New Products: ETF Express, Yahoo Finance
```

---

## Customization

### Search for Specific ETFs
Edit `fetch_etf_news_multiday.py` line 52:
```python
# Change from:
results = gn.get_news('intitle:ETF')

# To search specific tickers:
results = gn.get_news('THD OR GLD')
```

### Change Date Range
```bash
.venv/bin/python run_publisher_analysis.py 7  # 7 days instead of 3
```

### Filter by Topic
The analyzer automatically categorizes by:
- Bitcoin/Crypto
- Vanguard, BlackRock, iShares
- Dividends, Bonds, Precious Metals
- Investment Advice, Product News, Market Data

---

## Data Structure

### JSON Format (`etf_news_3days.json`)
```json
{
  "search_query": "intitle:ETF",
  "total_results": 100,
  "fetched_at": "2026-02-07T...",
  "date_range": {
    "days_covered": 8,
    "dates": ["2026-02-07", "2026-02-06", ...]
  },
  "articles": [
    {
      "title": "Article title...",
      "source": "Publisher name",
      "published": "Date string",
      "url": "https://...",
      "description": "Article summary..."
    }
  ]
}
```

---

## Next Time You Want This

**Simply ask Claude:**
> "Run the publisher analysis for 3 days"

**Or:**
> "Analyze ETF publishers from the last week"

**Claude will:**
1. Run `run_publisher_analysis.py`
2. Show you the analysis
3. Highlight publishers matching your interests

---

## Troubleshooting

### "Module not found"
```bash
# Reinstall dependencies
uv pip install gnews beautifulsoup4 lxml pandas
```

### "No virtual environment"
```bash
# Recreate venv
uv venv
uv pip install gnews beautifulsoup4 lxml pandas
```

### Want more articles?
The tool fetches in batches of 100. If you need more:
```bash
.venv/bin/python fetch_etf_news_multiday.py 7  # More days = more articles
```

---

## Dependencies

- **Python 3.11+**
- **uv** (package manager)
- **gnews** (Google News API)
- **pandas** (data analysis)
- **beautifulsoup4, lxml** (HTML parsing)

---

## Directory Structure

```
google_news/
├── README.md                          # This file
├── run_publisher_analysis.py          # ONE-CLICK runner
├── fetch_etf_news_multiday.py         # Fetch articles
├── analyze_publishers.py              # Analyze publishers
├── etf_news_3days.json               # Data (auto-generated)
├── publisher_report.md               # Report (auto-generated)
├── .venv/                            # Virtual environment
└── requirements.txt                  # Dependencies
```

---

## Quick Reference

| I Want To... | Command |
|-------------|---------|
| Get 3-day publisher analysis | `.venv/bin/python run_publisher_analysis.py` |
| Get 7-day publisher analysis | `.venv/bin/python run_publisher_analysis.py 7` |
| Just fetch data | `.venv/bin/python fetch_etf_news_multiday.py 3` |
| Analyze saved data | `.venv/bin/python analyze_publishers.py` |
| Search specific ETFs | Edit script, change `'intitle:ETF'` to `'THD OR GLD'` |

---

## Output Files

After running, you'll have:
- **`etf_news_3days.json`** - All article data
- **`publisher_report.md`** - Formatted analysis report
- **Console output** - Quick summary

All data is saved locally. No API keys needed. Free to use.
