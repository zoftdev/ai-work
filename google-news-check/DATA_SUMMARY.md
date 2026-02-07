# ETF News Data - Local Analysis Files

## Overview
All ETF news data has been retrieved and saved locally for analysis.

**Data Retrieved:** February 7, 2026
**Total Articles:** 50 articles with "ETF" in title
**Data Files:** 3 files (JSON and CSV formats)

---

## Files Available

### 1. `etf_news_results.json` (31 KB)
**Original data from Google News**

Contains:
- Article titles
- Source/publisher names
- Publication dates
- Google News URLs
- Article descriptions/snippets

**Use for:** Basic metadata analysis, source distribution, timeline analysis

---

### 2. `etf_news_full_data.json` (48 KB)
**Enriched data with additional fields**

Contains everything from #1 plus:
- Authors (when available)
- Article publish dates
- Top images
- Keywords
- Fetch status
- Word counts

**Use for:** Comprehensive analysis, data mining, correlation studies

**Format:**
```json
{
  "search_query": "intitle:ETF",
  "total_results": 50,
  "fetched_at": "2026-02-07T11:59:xx",
  "enriched_at": "2026-02-07T12:05:xx",
  "articles": [...]
}
```

---

### 3. `etf_news_analysis.csv` (26 KB)
**Tabular format for spreadsheet analysis**

Columns:
- title
- source
- published
- url
- word_count
- authors
- fetch_success
- description

**Use for:**
- Import into Excel, Google Sheets, or Pandas
- Quick filtering and sorting
- Pivot tables
- Visualization tools

---

## Data Statistics

### Source Distribution (Top 10)
1. The Motley Fool: 8 articles
2. ETF Express: 4 articles
3. Seeking Alpha: 3 articles
4. 24/7 Wall St.: 3 articles
5. ETF.com: 2 articles
6. Yahoo Finance: 2 articles
7. morningstar.com: 2 articles
8. Business Wire: 2 articles
9. CoinDesk: 2 articles
10. Stock Traders Daily: 2 articles

**Total unique sources:** 29

### Content Categories (from titles)
- Bitcoin/Crypto ETFs: ~12 articles
- Vanguard ETFs: ~8 articles
- Sector/Thematic ETFs: ~10 articles
- Market Analysis: ~15 articles
- ETF Industry News: ~5 articles

---

## Analysis Recommendations

### Python Analysis
```python
import pandas as pd
import json

# Load CSV for quick analysis
df = pd.read_csv('etf_news_analysis.csv')

# Or load JSON for detailed analysis
with open('etf_news_full_data.json') as f:
    data = json.load(f)
```

### Possible Analyses
1. **Source Analysis** - Which publishers cover ETF news most?
2. **Temporal Analysis** - Publication patterns over time
3. **Topic Analysis** - Extract themes from titles/descriptions
4. **Sentiment Analysis** - Analyze tone of headlines
5. **Network Analysis** - Connect related topics/sources

### Keywords to Extract
- ETF tickers (JEPI, MTUM, SMLF, etc.)
- Companies (BlackRock, Vanguard, iShares)
- Asset classes (Bitcoin, Gold, Silver, Bonds)
- Strategies (Dividend, Value, Growth, Low Vol)

---

## Next Steps

### To Query Specific ETFs (e.g., THD, GLD):
```python
# Modify fetch_etf_news.py line 19:
search_query = 'THD OR GLD'
# Then run: .venv/bin/python fetch_etf_news.py
```

### To Fetch More Articles:
```python
# Modify fetch_etf_news.py line 13:
google_news = GNews(
    language='en',
    country='US',
    max_results=100  # Increase from 50
)
```

### To Get Full Article Text:
Note: Google News URLs are redirects. To get full text:
1. Extract actual URLs from Google News redirects
2. Use web scraping with BeautifulSoup
3. Or use paid APIs (NewsAPI, GNews API) that provide full content

---

## File Locations
```
/Users/thisadee_pre/play/google_news/
├── etf_news_results.json       (Original data)
├── etf_news_full_data.json     (Enriched data)
├── etf_news_analysis.csv       (CSV for analysis)
├── fetch_etf_news.py           (Main scraper)
├── fetch_full_articles.py      (Article content fetcher)
└── DATA_SUMMARY.md             (This file)
```

---

**Ready for analysis!** All files are in standard formats (JSON/CSV) compatible with:
- Python (Pandas, NumPy, Matplotlib)
- R
- Excel/Google Sheets
- Tableau/Power BI
- Jupyter Notebooks
