import urllib.request
import json
import urllib.parse
import time

repos = [
    'freeCodeCamp/freeCodeCamp',
    'appsmithorg/appsmith',
    'calcom/cal.com',
    'mattermost/mattermost',
    'zulip/zulip',
    'novuhq/novu',
    'RocketChat/Rocket.Chat',
    'hoppscotch/hoppscotch',
    'elastic/elasticsearch',
    'vercel/next.js',
    'mui/material-ui'
]

print("Fetching issues from GUARANTEED 10,000+ Star Repositories...\n")

valid_issues = []

for repo in repos:
    # 0 assignees, 0 comments, open issue
    query = f'repo:{repo} is:issue is:open no:assignee comments:0'
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=3'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            for item in items:
                # Double check it isn't a PR
                if 'pull_request' not in item:
                    valid_issues.append({
                        'repo': repo,
                        'title': item.get('title'),
                        'url': item.get('html_url')
                    })
    except Exception as e:
        pass
    
    time.sleep(1) # Prevent rate limiting

for issue in valid_issues[:10]:
    print(f"[{issue['repo']}]")
    print(f"Title: {issue['title']}")
    print(f"URL: {issue['url']}")
    print("-" * 40)

