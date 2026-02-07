#!/usr/bin/env python3
"""
Analyze ETF news publishers to identify sources of interest
"""

import json
from collections import Counter, defaultdict
import re

def load_data(filename='etf_news_3days.json'):
    """Load the ETF news data"""
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_publisher_coverage(articles):
    """Analyze what each publisher covers"""

    publisher_articles = defaultdict(list)

    for article in articles:
        source = article['source']
        publisher_articles[source].append({
            'title': article['title'],
            'date': article['published']
        })

    return publisher_articles

def extract_topics_from_title(title):
    """Extract topics/keywords from article title"""
    topics = []

    title_lower = title.lower()

    # ETF providers
    if 'vanguard' in title_lower:
        topics.append('Vanguard')
    if 'ishares' in title_lower or 'blackrock' in title_lower:
        topics.append('iShares/BlackRock')
    if 'spdr' in title_lower or 's&p' in title_lower:
        topics.append('SPDR/S&P')

    # Asset classes
    if 'bitcoin' in title_lower or 'crypto' in title_lower or 'btc' in title_lower:
        topics.append('Bitcoin/Crypto')
    if 'gold' in title_lower or 'silver' in title_lower:
        topics.append('Precious Metals')
    if 'bond' in title_lower or 'treasury' in title_lower or 'fixed income' in title_lower:
        topics.append('Bonds')

    # Strategies
    if 'dividend' in title_lower:
        topics.append('Dividend')
    if 'value' in title_lower:
        topics.append('Value')
    if 'growth' in title_lower:
        topics.append('Growth')
    if 'momentum' in title_lower:
        topics.append('Momentum')
    if 'covered call' in title_lower:
        topics.append('Covered Call')

    # Sectors
    if 'tech' in title_lower or 'software' in title_lower:
        topics.append('Technology')
    if 'healthcare' in title_lower or 'health' in title_lower:
        topics.append('Healthcare')
    if 'energy' in title_lower:
        topics.append('Energy')

    # Geography
    if 'china' in title_lower or 'chinese' in title_lower:
        topics.append('China')
    if 'international' in title_lower or 'global' in title_lower or 'emerging' in title_lower:
        topics.append('International')

    # Content type
    if any(word in title_lower for word in ['buy', 'sell', 'invest', 'portfolio']):
        topics.append('Investment Advice')
    if any(word in title_lower for word in ['launches', 'announces', 'files', 'debuts']):
        topics.append('Product News')
    if any(word in title_lower for word in ['flows', 'inflows', 'volume', 'assets']):
        topics.append('Market Data')

    return topics if topics else ['General']

def analyze_publisher_focus(publisher_articles):
    """Analyze what topics each publisher focuses on"""

    publisher_topics = defaultdict(Counter)

    for publisher, articles in publisher_articles.items():
        for article in articles:
            topics = extract_topics_from_title(article['title'])
            for topic in topics:
                publisher_topics[publisher][topic] += 1

    return publisher_topics

def rank_publishers(articles):
    """Rank publishers by various metrics"""

    # Count articles per publisher
    publisher_counts = Counter(a['source'] for a in articles)

    # Analyze topics
    publisher_articles = analyze_publisher_coverage(articles)
    publisher_topics = analyze_publisher_focus(publisher_articles)

    # Calculate diversity score (how many different topics they cover)
    publisher_diversity = {
        pub: len(topics) for pub, topics in publisher_topics.items()
    }

    return publisher_counts, publisher_topics, publisher_diversity

def main():
    print("\n" + "="*80)
    print("PUBLISHER ANALYSIS - Find Your Interest")
    print("="*80)

    data = load_data()
    articles = data['articles']

    print(f"\nAnalyzing {len(articles)} articles from {data['date_range']['days_covered']} days")
    print(f"Date range: {data['date_range']['dates'][-1]} to {data['date_range']['dates'][0]}")

    # Get publisher statistics
    publisher_counts, publisher_topics, publisher_diversity = rank_publishers(articles)

    print("\n" + "="*80)
    print("TOP PUBLISHERS BY VOLUME")
    print("="*80)

    for i, (publisher, count) in enumerate(publisher_counts.most_common(20), 1):
        diversity = publisher_diversity.get(publisher, 0)
        print(f"{i:2d}. {publisher:40s} {count:3d} articles, {diversity:2d} topics")

    print("\n" + "="*80)
    print("PUBLISHERS BY SPECIALIZATION")
    print("="*80)

    # Group publishers by their main topics
    topic_specialists = defaultdict(list)

    for publisher, topics in publisher_topics.items():
        # Get top 3 topics for this publisher
        top_topics = topics.most_common(3)
        for topic, count in top_topics:
            if count >= 2:  # At least 2 articles on this topic
                topic_specialists[topic].append((publisher, count))

    for topic in sorted(topic_specialists.keys()):
        publishers = sorted(topic_specialists[topic], key=lambda x: x[1], reverse=True)
        print(f"\n{topic}:")
        for pub, count in publishers[:5]:  # Top 5 per topic
            print(f"  - {pub}: {count} articles")

    print("\n" + "="*80)
    print("PUBLISHER PROFILES")
    print("="*80)

    # Detailed profile for top 10 publishers
    for publisher, count in publisher_counts.most_common(10):
        print(f"\n{publisher} ({count} articles)")
        print("-" * 60)

        # Show their topic coverage
        topics = publisher_topics[publisher]
        print("Topics covered:")
        for topic, topic_count in topics.most_common(5):
            pct = (topic_count / count) * 100
            print(f"  {topic:25s} {topic_count:2d} articles ({pct:4.1f}%)")

        # Show sample headlines
        articles_by_pub = [a for a in articles if a['source'] == publisher]
        print("\nSample headlines:")
        for article in articles_by_pub[:3]:
            title = article['title'][:70] + "..." if len(article['title']) > 70 else article['title']
            print(f"  • {title}")

    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    print("\nBased on coverage patterns, consider these publishers for:")

    print("\n📊 Comprehensive ETF Coverage:")
    for pub, count in publisher_counts.most_common(5):
        print(f"  • {pub} ({count} articles)")

    print("\n🎯 Specific Investment Advice:")
    advice_pubs = [(p, c) for p, c in publisher_counts.items()
                   if 'Investment Advice' in publisher_topics[p]]
    for pub, _ in sorted(advice_pubs, key=lambda x: publisher_topics[x[0]]['Investment Advice'], reverse=True)[:3]:
        count = publisher_topics[pub]['Investment Advice']
        print(f"  • {pub} ({count} advice articles)")

    print("\n📈 Market Data & Analysis:")
    data_pubs = [(p, c) for p, c in publisher_counts.items()
                 if 'Market Data' in publisher_topics[p]]
    for pub, _ in sorted(data_pubs, key=lambda x: publisher_topics[x[0]]['Market Data'], reverse=True)[:3]:
        count = publisher_topics[pub]['Market Data']
        print(f"  • {pub} ({count} data articles)")

    print("\n🆕 New Product Launches:")
    product_pubs = [(p, c) for p, c in publisher_counts.items()
                    if 'Product News' in publisher_topics[p]]
    for pub, _ in sorted(product_pubs, key=lambda x: publisher_topics[x[0]]['Product News'], reverse=True)[:3]:
        count = publisher_topics[pub]['Product News']
        print(f"  • {pub} ({count} product news)")

    print("\n" + "="*80)
    print("\n✓ Analysis complete!")
    print("\nNext steps:")
    print("  1. Review publisher profiles above")
    print("  2. Check etf_news_3days.json for full data")
    print("  3. Run fetch_etf_news_multiday.py to get more days if needed")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
