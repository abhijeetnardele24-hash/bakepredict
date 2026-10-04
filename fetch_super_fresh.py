import urllib.request
import json
import urllib.parse
from datetime import datetime, timedelta

# Search for issues created strictly in the last 24 hours, no comments, no assignee
query = 'is:issue is:open no:assignee comments:0 stars:>100 created:>2026-09-29T10:00:00Z'
encoded_query = urllib.parse.quote(query)
url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=10'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
print("Hunting for absolute freshest issues (0 comments, created very recently)...")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])
        found = 0
        for item in items:
            repo_url = item.get('repository_url', '').replace('https://api.github.com/repos/', '')
            # Filter out some common bot/spam repos if they appear, but mostly just print the good ones
            print(f"\n[{repo_url}]")
            print(f"Title: {item.get('title')}")
            print(f"URL: {item.get('html_url')}")
            print(f"Created At: {item.get('created_at')}")
            found += 1
            if found >= 5:
                break
        if not found:
            print("No issues found in this window.")
except Exception as e:
    print(f'Error: {e}')
