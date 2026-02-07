#!/usr/bin/env python3
"""
Quick analysis of ETF news data
"""

import json
import pandas as pd
from collections import Counter
from datetime import datetime
import re

def load_data():
    """Load the ETF news data"""
    with open('etf_news_full_data.json', 'r') as f:
        return json.load(f)

def analyze_sources(articles):
    """Analyze source distribution"""
    sources = [a['source'] for a in articles]
    source_counts = Counter(sources)

    print("\n" + "="*60)
    print("SOURCE ANALYSIS")
    print("="*60)
    print(f"Total unique sources: {len(source_counts)}")
    print(f"\nTop 10 sources:")
    for source, count in source_counts.most_common(10):
        print(f"  {count:2d}  {source}")

def analyze_dates(articles):
    """Analyze publication dates"""
    print("\n" + "="*60)
    print("DATE ANALYSIS")
    print("="*60)

    dates = []
    for a in articles:
        if a['published']:
            # Parse the date string
            try:
                date_str = a['published']
                # Extract just the date part
                if ',' in date_str:
                    parts = date_str.split(',')
                    if len(parts) >= 2:
                        dates.append(parts[1].strip().split()[0])
            except:
                pass

    date_counts = Counter(dates)
    print(f"Articles by date:")
    for date, count in sorted(date_counts.items()):
        print(f"  {date}: {count} articles")

def extract_etf_tickers(articles):
    """Extract ETF ticker symbols from titles"""
    print("\n" + "="*60)
    print("ETF TICKERS MENTIONED")
    print("="*60)

    # Common ETF ticker patterns
    tickers = []
    for a in articles:
        title = a['title']
        # Find capitalized words 2-5 letters long (likely tickers)
        matches = re.findall(r'\b[A-Z]{2,5}\b', title)
        tickers.extend(matches)

    ticker_counts = Counter(tickers)
    # Filter out common words
    common_words = {'ETF', 'US', 'USA', 'UK', 'CEO', 'API', 'USD', 'THE'}

    print("Top ticker mentions:")
    for ticker, count in ticker_counts.most_common(20):
        if ticker not in common_words and count > 1:
            print(f"  {ticker}: {count} times")

def analyze_topics(articles):
    """Analyze topics from titles"""
    print("\n" + "="*60)
    print("TOPIC ANALYSIS")
    print("="*60)

    # Keywords to look for
    topics = {
        'Bitcoin/Crypto': ['bitcoin', 'crypto', 'blockchain'],
        'Vanguard': ['vanguard'],
        'BlackRock': ['blackrock'],
        'iShares': ['ishares'],
        'Gold/Silver': ['gold', 'silver'],
        'Dividend': ['dividend'],
        'Bond': ['bond', 'treasury'],
        'International': ['china', 'international', 'global', 'emerging'],
        'Sector': ['tech', 'healthcare', 'software', 'space'],
        'Strategy': ['momentum', 'value', 'growth', 'volatility', 'vol']
    }

    topic_counts = {topic: 0 for topic in topics}

    for a in articles:
        title_lower = a['title'].lower()
        for topic, keywords in topics.items():
            if any(keyword in title_lower for keyword in keywords):
                topic_counts[topic] += 1

    print("Articles by topic:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {topic}: {count} articles")

def create_summary_stats(data):
    """Create overall summary statistics"""
    articles = data['articles']

    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"Search query: {data['search_query']}")
    print(f"Data fetched: {data['fetched_at']}")
    print(f"Total articles: {data['total_results']}")
    print(f"Successfully processed: {len(articles)}")

def export_for_analysis():
    """Export data in analysis-friendly format"""
    df = pd.read_csv('etf_news_analysis.csv')

    print("\n" + "="*60)
    print("PANDAS DATAFRAME INFO")
    print("="*60)
    print(df.info())

    print("\n" + "="*60)
    print("SAMPLE RECORDS")
    print("="*60)
    print(df[['title', 'source', 'published']].head())

def main():
    print("\nETF NEWS DATA ANALYSIS")
    print("="*60)

    # Load data
    data = load_data()
    articles = data['articles']

    # Run analyses
    create_summary_stats(data)
    analyze_sources(articles)
    analyze_dates(articles)
    analyze_topics(articles)
    extract_etf_tickers(articles)

    # Pandas analysis
    try:
        export_for_analysis()
    except Exception as e:
        print(f"\nNote: Install pandas for dataframe analysis: uv pip install pandas")

    print("\n" + "="*60)
    print("Analysis complete! Data files available:")
    print("  - etf_news_full_data.json (complete data)")
    print("  - etf_news_analysis.csv (for spreadsheets)")
    print("  - DATA_SUMMARY.md (documentation)")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
