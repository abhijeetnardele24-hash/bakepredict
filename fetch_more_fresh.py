import urllib.request
import json
import urllib.parse
import time

repos = [
    'appsmithorg/appsmith',
    'mattermost/mattermost',
    'hoppscotch/hoppscotch',
    'RocketChat/Rocket.Chat',
    'home-assistant/core',
    'mui/material-ui',
    'vercel/next.js',
    'elastic/elasticsearch'
]

print("Hunting for fresh 0-comment issues across top open-source repositories...\n")

for repo in repos:
    query = f'repo:{repo} is:issue is:open no:assignee comments:0'
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=2'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            if items:
                print(f'### 🌟 {repo.upper()}')
                for item in items:
                    print(f"* **{item.get('title')}**\n  * URL: {item.get('html_url')}")
                print()
    except Exception as e:
        pass
    time.sleep(1) # Prevent rate limiting
