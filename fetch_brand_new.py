import urllib.request
import json
import urllib.parse

query = 'is:issue is:open no:assignee comments:0 label:bug stars:>100 created:>2026-09-27'
encoded_query = urllib.parse.quote(query)
url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=5'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])
        for item in items:
            repo_url = item.get('repository_url', '').replace('https://api.github.com/repos/', '')
            print(f"[{repo_url}]")
            print(f"Title: {item.get('title')}")
            print(f"URL: {item.get('html_url')}")
            print(f"Created: {item.get('created_at')}")
            print("-" * 40)
except Exception as e:
    pass
