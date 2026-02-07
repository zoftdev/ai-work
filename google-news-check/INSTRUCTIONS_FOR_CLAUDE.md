# Instructions for Claude - Next Session

## User Request Pattern

When the user says:
- **"Run the publisher analysis for 3 days"**
- **"Analyze ETF publishers"**
- **"Review 3 days of ETF news publishers"**

## What to Do

### Step 1: Run the Analysis
```bash
.venv/bin/python run_publisher_analysis.py
```

Or with custom days:
```bash
.venv/bin/python run_publisher_analysis.py 7  # for 7 days
```

### Step 2: Present Results

Show the user:

1. **Top Publishers by Volume**
   - List top 10-15 publishers
   - Show article count and topic diversity

2. **Publishers by Specialization**
   - Bitcoin/Crypto specialists
   - Investment Advice publishers
   - Market Data sources
   - Product News sources

3. **Publisher Profiles** (Top 5-10)
   - What topics they cover (with percentages)
   - Sample headlines
   - Focus areas

4. **Recommendations**
   - 📊 Comprehensive Coverage
   - 🎯 Investment Advice
   - 📈 Market Data
   - 🆕 Product Launches
   - 💰 Bitcoin/Crypto
   - (any other relevant categories)

### Step 3: Summary

End with:
```
✓ Analysis complete!

Files saved:
- etf_news_3days.json (raw data with X articles)
- All data saved locally for further analysis

Top recommendations:
- For comprehensive coverage: [top 3]
- For investment advice: [top 3]
- For [specific interest]: [top 3]
```

---

## File Structure

### Core Scripts (These Work)
- `run_publisher_analysis.py` - ONE-CLICK main script
- `fetch_etf_news_multiday.py` - Fetch articles for N days
- `analyze_publishers.py` - Analyze publisher data

### Documentation
- `QUICKSTART.md` - User-facing quick guide
- `README.md` - Complete documentation
- `INSTRUCTIONS_FOR_CLAUDE.md` - This file

### Data Files (Auto-generated)
- `etf_news_3days.json` - Article data
- Any other JSON files with article data

### Old/Legacy Files (Can ignore)
- `fetch_etf_news.py` - Old single-run fetcher
- `fetch_full_articles.py` - Old full-text fetcher
- `analyze_etf_data.py` - Old general analyzer
- `etf_news_results.json` - Old data
- `etf_news_full_data.json` - Old data
- `etf_news_analysis.csv` - Old data
- `DATA_SUMMARY.md` - Old documentation

---

## Common Variations

### "Get more days"
```bash
.venv/bin/python run_publisher_analysis.py 7
```

### "Search specific ETFs"
Edit `fetch_etf_news_multiday.py` line 52:
```python
results = gn.get_news('THD OR GLD')  # instead of 'intitle:ETF'
```

### "Just fetch data, no analysis"
```bash
.venv/bin/python fetch_etf_news_multiday.py 3
```

### "Analyze existing data"
```bash
.venv/bin/python analyze_publishers.py
```

---

## Response Template

Use this template for responses:

```
Running publisher analysis for [N] days...

[Show output from run_publisher_analysis.py]

## Key Findings

**Top 3 Publishers:**
1. [Publisher] - [X] articles ([focus areas])
2. [Publisher] - [X] articles ([focus areas])
3. [Publisher] - [X] articles ([focus areas])

## Recommendations by Interest

**For [Interest 1]:**
- [Publisher] ([X] articles)
- [Publisher] ([X] articles)

**For [Interest 2]:**
- [Publisher] ([X] articles)

[etc.]

## Data Saved

All data in: etf_news_[N]days.json
Total articles: [X]
Date range: [dates]

You now have complete publisher data to identify your interests!
```

---

## Error Handling

### If script fails:
1. Check internet connection
2. Try: `uv pip install -r requirements.txt`
3. Recreate venv: `uv venv && uv pip install -r requirements.txt`

### If no data file exists:
Run fetch first: `.venv/bin/python fetch_etf_news_multiday.py 3`

---

## Key Points

- Always run `run_publisher_analysis.py` (it handles everything)
- Default is 3 days, can customize
- Results show publisher specializations
- All data saved locally (JSON format)
- No API keys needed, free to use
- GNews library limits: ~100 articles per search

---

## User Intent Recognition

User says → Action:
- "analyze publishers" → Run analysis
- "get ETF news" → Run analysis
- "review publishers" → Run analysis
- "3 days" → Use 3 as parameter
- "last week" → Use 7 as parameter
- "THD and GLD" → Modify search query

---

## End Goal

User gets clear answer about which publishers to follow based on their interests in ETF news coverage.
