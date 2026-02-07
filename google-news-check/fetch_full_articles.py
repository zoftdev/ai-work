#!/usr/bin/env python3
"""
Fetch full article content for all ETF news articles
"""

import json
import time
from newspaper import Article
from datetime import datetime
import csv

def fetch_article_content(url, title):
    """Fetch full article content from URL"""
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            'success': True,
            'text': article.text,
            'authors': article.authors,
            'publish_date': str(article.publish_date) if article.publish_date else None,
            'top_image': article.top_image,
            'keywords': article.keywords if hasattr(article, 'keywords') else [],
            'summary': article.summary if hasattr(article, 'summary') else ''
        }
    except Exception as e:
        print(f"   ⚠️  Failed to fetch: {title[:60]}...")
        print(f"      Error: {str(e)[:100]}")
        return {
            'success': False,
            'error': str(e),
            'text': '',
            'authors': [],
            'publish_date': None,
            'top_image': '',
            'keywords': [],
            'summary': ''
        }

def main():
    print("Loading existing ETF news data...")
    with open('etf_news_results.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    articles = data['articles']
    print(f"Found {len(articles)} articles to process\n")

    enriched_articles = []

    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] Fetching: {article['title'][:60]}...")

        # Fetch full content
        content = fetch_article_content(article['url'], article['title'])

        # Merge with existing data
        enriched_article = {
            **article,
            'full_text': content['text'],
            'authors': content['authors'],
            'article_publish_date': content['publish_date'],
            'top_image': content['top_image'],
            'keywords': content['keywords'],
            'article_summary': content['summary'],
            'fetch_success': content['success'],
            'fetch_error': content.get('error', ''),
            'word_count': len(content['text'].split()) if content['text'] else 0
        }

        enriched_articles.append(enriched_article)

        if content['success']:
            print(f"   ✓ Success - {enriched_article['word_count']} words")

        # Be polite to servers
        time.sleep(1)

    # Save enriched data to JSON
    output_data = {
        'search_query': data['search_query'],
        'total_results': len(enriched_articles),
        'fetched_at': data['fetched_at'],
        'enriched_at': datetime.now().isoformat(),
        'articles': enriched_articles
    }

    json_filename = 'etf_news_full_data.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Full data saved to: {json_filename}")

    # Save to CSV for easy analysis
    csv_filename = 'etf_news_analysis.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'source', 'published', 'url', 'word_count',
                      'authors', 'fetch_success', 'description']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for article in enriched_articles:
            writer.writerow({
                'title': article['title'],
                'source': article['source'],
                'published': article['published'],
                'url': article['url'],
                'word_count': article['word_count'],
                'authors': ', '.join(article['authors']) if article['authors'] else '',
                'fetch_success': article['fetch_success'],
                'description': article['description']
            })

    print(f"✓ CSV saved to: {csv_filename}")

    # Print statistics
    successful = sum(1 for a in enriched_articles if a['fetch_success'])
    failed = len(enriched_articles) - successful
    total_words = sum(a['word_count'] for a in enriched_articles)

    print(f"\n{'='*60}")
    print("Statistics:")
    print(f"  Total articles: {len(enriched_articles)}")
    print(f"  Successfully fetched: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total words: {total_words:,}")
    print(f"  Average words per article: {total_words//successful if successful > 0 else 0}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
