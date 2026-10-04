import urllib.request
import json
import urllib.parse

repos = ['zulip/zulip', 'novuhq/novu', 'calcom/cal.com', 'appwrite/appwrite', 'freeCodeCamp/freeCodeCamp']

print("Hunting for 100% untouched issues (0 assignees, 0 comments)...")

for repo in repos:
    query = f'repo:{repo} is:issue is:open no:assignee comments:0'
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=3'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            if items:
                print(f'\n--- {repo.upper()} ---')
                for item in items:
                    print(f"Title: {item.get('title')}")
                    print(f"URL: {item.get('html_url')}")
    except Exception as e:
        pass
