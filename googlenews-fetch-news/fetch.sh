#!/bin/bash
set -e

echo "🔍 Fetching article metadata from Google News..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
uv run python src/stage1_fetch.py "$@"

echo ""
echo "✓ Complete! Results saved to data/ (timestamped YAML)"
echo ""
echo "Next: Run external application for content fetching & summarization"
