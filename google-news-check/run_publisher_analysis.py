#!/usr/bin/env python3
"""
ONE-CLICK ETF Publisher Analysis

Usage:
    python run_publisher_analysis.py          # Analyze 3 days (default)
    python run_publisher_analysis.py 7        # Analyze 7 days
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("\n" + "="*80)
    print("ETF PUBLISHER ANALYSIS - ONE-CLICK RUN")
    print("="*80)

    # Get number of days from argument
    days = 3
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print("Usage: python run_publisher_analysis.py [days]")
            print("Using default: 3 days")

    print(f"\n📊 Running analysis for {days} days of ETF news...")

    # Step 1: Fetch articles
    print("\n" + "-"*80)
    print("STEP 1: Fetching articles from Google News...")
    print("-"*80)

    result = subprocess.run(
        [sys.executable, 'fetch_etf_news_multiday.py', str(days)],
        capture_output=False
    )

    if result.returncode != 0:
        print("\n❌ Error fetching articles. Check your internet connection.")
        return 1

    # Step 2: Analyze publishers
    print("\n" + "-"*80)
    print("STEP 2: Analyzing publishers...")
    print("-"*80)

    result = subprocess.run(
        [sys.executable, 'analyze_publishers.py'],
        capture_output=False
    )

    if result.returncode != 0:
        print("\n❌ Error analyzing publishers.")
        return 1

    # Done
    print("\n" + "="*80)
    print("✓ ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\n📁 Files created:")
    print(f"   - etf_news_{days}days.json (raw data)")
    print(f"\n💡 Next time, just tell Claude:")
    print(f'   "Run the publisher analysis for {days} days"')
    print("\n" + "="*80 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
