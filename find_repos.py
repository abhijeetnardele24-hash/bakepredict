import urllib.request
import json

url = 'https://api.github.com/search/issues?q=is:issue+is:open+no:assignee+label:%22good%20first%20issue%22+stars:100..5000+updated:%3E2026-09-20&sort=updated&order=desc&per_page=20'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])
        for item in items:
            repo_url = item.get('repository_url', '').replace('https://api.github.com/repos/', '')
            title = item.get('title', '')
            html_url = item.get('html_url', '')
            print(f'- Repo: {repo_url} | Issue: {title} | URL: {html_url}')
except Exception as e:
    print(f'Error: {e}')
