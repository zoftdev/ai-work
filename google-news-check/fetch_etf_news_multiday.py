#!/usr/bin/env python3
"""
Fetch ETF news articles covering multiple days
"""

from gnews import GNews
from datetime import datetime, timedelta
from collections import Counter
import json

def parse_date(date_str):
    """Parse date from Google News format"""
    try:
        # Format: "Fri, 06 Feb 2026 18:45:04 GMT"
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        return dt.date()
    except:
        return None

def fetch_articles_for_days(target_days=3, max_articles=500):
    """Fetch articles until we have coverage for target_days"""

    print(f"Fetching ETF news articles covering {target_days} days...")
    print("=" * 80)

    all_articles = []
    dates_seen = set()
    batch_size = 100

    for batch_num in range(1, (max_articles // batch_size) + 1):
        print(f"\nFetching batch {batch_num} (up to {batch_size} articles)...")

        gn = GNews(
            language='en',
            country='US',
            max_results=batch_size,
            start_date=(datetime.now() - timedelta(days=7)).date(),  # Last 7 days
            end_date=datetime.now().date()
        )

        # Search for articles with "ETF" in the title
        results = gn.get_news('intitle:ETF')

        if not results:
            print("No more results available")
            break

        # Process results
        new_articles = 0
        for article in results:
            # Skip duplicates
            if article['url'] not in [a['url'] for a in all_articles]:
                all_articles.append(article)
                new_articles += 1

                # Track dates
                date = parse_date(article.get('published date', ''))
                if date:
                    dates_seen.add(date)

        print(f"  Added {new_articles} new articles")
        print(f"  Total articles: {len(all_articles)}")
        print(f"  Unique dates covered: {len(dates_seen)}")

        # Check if we have enough days
        if len(dates_seen) >= target_days and len(all_articles) >= target_days * 30:
            print(f"\n✓ Reached {len(dates_seen)} days of coverage with {len(all_articles)} articles")
            break

        # If we got fewer results than requested, we've hit the limit
        if len(results) < batch_size:
            print("\n✓ Reached end of available articles")
            break

    return all_articles, dates_seen

def main():
    import sys

    target_days = 3
    if len(sys.argv) > 1:
        try:
            target_days = int(sys.argv[1])
        except ValueError:
            pass

    articles, dates_seen = fetch_articles_for_days(target_days)

    print("\n" + "=" * 80)
    print(f"COLLECTION SUMMARY")
    print("=" * 80)
    print(f"Total articles collected: {len(articles)}")
    print(f"Date range covered: {len(dates_seen)} unique dates")

    # Show date distribution
    date_counts = Counter()
    for article in articles:
        date = parse_date(article.get('published date', ''))
        if date:
            date_counts[date] += 1

    print(f"\nArticles by date:")
    for date in sorted(date_counts.keys(), reverse=True):
        print(f"  {date}: {date_counts[date]} articles")

    # Source distribution
    sources = [a['publisher']['title'] for a in articles if 'publisher' in a]
    source_counts = Counter(sources)

    print(f"\nTop 20 publishers:")
    for source, count in source_counts.most_common(20):
        print(f"  {count:3d}  {source}")

    print(f"\nTotal unique publishers: {len(source_counts)}")

    # Save to file
    output_data = {
        'search_query': 'intitle:ETF',
        'total_results': len(articles),
        'fetched_at': datetime.now().isoformat(),
        'date_range': {
            'days_covered': len(dates_seen),
            'dates': [str(d) for d in sorted(dates_seen, reverse=True)]
        },
        'articles': []
    }

    for article in articles:
        output_data['articles'].append({
            'title': article.get('title', ''),
            'source': article.get('publisher', {}).get('title', ''),
            'published': article.get('published date', ''),
            'url': article.get('url', ''),
            'description': article.get('description', '')
        })

    filename = f'etf_news_{target_days}days.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Data saved to: {filename}")
    print("=" * 80)

if __name__ == "__main__":
    main()
