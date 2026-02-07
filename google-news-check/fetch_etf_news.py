#!/usr/bin/env python3
"""
Fetch the last 50 Google News articles with 'ETF' in the title
"""

from gnews import GNews
from datetime import datetime
import json

def fetch_etf_news(max_results=100):
    """Fetch Google News articles with ETF in title"""
    # Initialize GNews with parameters
    google_news = GNews(
        language='en',
        country='US',
        max_results=max_results  # Configurable limit
    )

    # Search for articles with "ETF" in the title
    search_query = 'intitle:ETF'

    print(f"Searching Google News for: {search_query}")
    print("=" * 80)

    try:
        # Perform the search
        articles = google_news.get_news(search_query)

        print(f"\nFound {len(articles)} articles with 'ETF' in the title\n")

        # Display articles
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            publisher = article.get('publisher', {}).get('title', 'Unknown source')
            published_date = article.get('published date', 'No date')
            url = article.get('url', 'No link')

            print(f"{i}. {title}")
            print(f"   Source: {publisher}")
            print(f"   Published: {published_date}")
            print(f"   Link: {url}")
            print()

        # Save to JSON file
        output_data = {
            'search_query': search_query,
            'total_results': len(articles),
            'fetched_at': datetime.now().isoformat(),
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

        # Save to file
        with open('etf_news_results.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: etf_news_results.json")

    except Exception as e:
        print(f"Error fetching news: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys

    # Get max_results from command line argument or use default
    max_results = 100  # Default

    if len(sys.argv) > 1:
        try:
            max_results = int(sys.argv[1])
            print(f"Fetching up to {max_results} articles...")
        except ValueError:
            print("Usage: python fetch_etf_news.py [max_results]")
            print("Using default: 100 articles")

    fetch_etf_news(max_results)
