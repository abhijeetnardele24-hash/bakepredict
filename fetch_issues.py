import urllib.request
import json
import urllib.parse

def fetch_issues(repo):
    query = f'repo:{repo} is:issue is:open no:assignee label:bug'
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=5'
    
    print(f'\n--- {repo.upper()} ISSUES (bug, unassigned) ---')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            for item in items:
                print(f"Title: {item.get('title')}")
                print(f"URL: {item.get('html_url')}")
                print('-' * 40)
    except Exception as e:
        print(f'Error: {e}')

fetch_issues('zulip/zulip')
fetch_issues('novuhq/novu')
