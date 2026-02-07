# QUICKSTART - For Next Time

## What You Want

**Analyze ETF news publishers to see which ones you'd be interested in.**

---

## Tell Claude This:

```
Run the publisher analysis for 3 days
```

**Or:**

```
Analyze ETF publishers from the last week
```

---

## What Claude Will Do

Claude will run:
```bash
.venv/bin/python run_publisher_analysis.py
```

**This:**
1. ✓ Fetches 100+ ETF news articles from last 3 days
2. ✓ Analyzes all publishers (who covers what)
3. ✓ Shows you recommendations

---

## You'll Get

### 1. Top Publishers by Volume
```
ETF Trends:        25 articles
Yahoo Finance:     21 articles
The Motley Fool:   18 articles
```

### 2. Publishers by Interest
```
📊 Comprehensive Coverage: ETF Trends, Yahoo Finance
🎯 Investment Advice: The Motley Fool, Yahoo Finance
💰 Bitcoin/Crypto: CoinDesk
🆕 New Products: ETF Express
```

### 3. Publisher Profiles
For each major publisher:
- What topics they cover
- Sample headlines
- Coverage percentages

---

## Files Created

- `etf_news_3days.json` - All article data
- Console output - Analysis summary

---

## Custom Requests

**More days:**
```
Run publisher analysis for 7 days
```

**Specific ETFs:**
```
Fetch news for THD and GLD ETFs
```

---

## That's It!

Next time, just open this folder and ask Claude to run the analysis.

No need to remember commands or file names.
