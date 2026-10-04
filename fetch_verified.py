import urllib.request
import json
import urllib.parse
import time

query = 'is:issue is:open no:assignee comments:0 label:bug stars:>100 created:>2026-09-29'
encoded_query = urllib.parse.quote(query)
url = f'https://api.github.com/search/issues?q={encoded_query}&sort=created&order=desc&per_page=30'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    print("Fetching issues and VERIFYING star counts...")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])
        valid_issues = []
        
        for item in items:
            repo_url = item.get('repository_url')
            # Fetch repo details to confirm star count
            repo_req = urllib.request.Request(repo_url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                with urllib.request.urlopen(repo_req) as r_response:
                    r_data = json.loads(r_response.read().decode())
                    stars = r_data.get('stargazers_count', 0)
                    if stars >= 100:
                        valid_issues.append({
                            'repo': r_data.get('full_name'),
                            'stars': stars,
                            'title': item.get('title'),
                            'url': item.get('html_url'),
                            'created': item.get('created_at')
                        })
                        print(f"Found valid repo: {r_data.get('full_name')} with {stars} stars!")
                    else:
                        print(f"Skipping {r_data.get('full_name')}, only has {stars} stars.")
            except Exception as e:
                pass
            
            if len(valid_issues) >= 5:
                break
            time.sleep(0.5) # rate limit prevention

        print("\n--- FINAL VERIFIED LIST ---")
        for issue in valid_issues:
            print(f"[{issue['repo']}] (Stars: {issue['stars']})")
            print(f"Title: {issue['title']}")
            print(f"URL: {issue['url']}")
            print("-" * 40)
except Exception as e:
    print(f'Error: {e}')
