import urllib.request
import json
import urllib.parse
from datetime import datetime

repos = [
    'calcom/cal.com',
    'mattermost/mattermost',
    'zulip/zulip',
    'novuhq/novu',
    'appsmithorg/appsmith',
    'freeCodeCamp/freeCodeCamp',
    'home-assistant/core',
    'appwrite/appwrite',
    'mui/material-ui',
    'supabase/supabase'
]

print("Fetching strictly NEW issues (Created in the last 48 hours)...\n")

for repo in repos:
    # Adding created filter strictly to 2026-09-29 and 2026-09-30
    query = f'repo:{repo} is:issue is:open no:assignee comments:0 created:>2026-09-28T00:00:00Z'
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=3'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            for item in items:
                if 'pull_request' not in item:
                    print(f"[{repo}]")
                    print(f"Title: {item.get('title')}")
                    print(f"URL: {item.get('html_url')}")
                    print(f"Date: {item.get('created_at')}")
                    print("-" * 40)
    except Exception as e:
        pass
