$recent_date = (Get-Date).AddDays(-14).ToString("yyyy-MM-dd")
$query = "is:issue is:open label:`"help wanted`" no:assignee comments:0 created:>$recent_date"
$encoded_query = [uri]::EscapeDataString($query)

$valid_issues = @()
$repo_counts = @{}
$page = 1

while ($valid_issues.Count -lt 20 -and $page -le 3) {
    Write-Host "Searching page $page for fresh, 0-comment issues created in the last 7 days..."
    $search_url = "/search/issues?q=$encoded_query&sort=created&order=desc&per_page=100&page=$page"
    $issues = gh api $search_url | ConvertFrom-Json
    
    if ($issues.items.Count -eq 0) {
        break
    }


foreach ($issue in $issues.items) {
    if ($valid_issues.Count -ge 20) {
        break
    }
    
    # Extract repository path from the repository URL
    $repo_url = $issue.repository_url
    $repo_path = $repo_url -replace "https://api.github.com/repos/", ""
    
    if (-not $repo_counts.ContainsKey($repo_path)) {
        $repo_counts[$repo_path] = 0
    }
    
    if ($repo_counts[$repo_path] -ge 3) {
        continue
    }
    
    # Query repository to check its star count
    try {
        $repo_info = gh api "/repos/$repo_path" | ConvertFrom-Json
        if ($repo_info.stargazers_count -ge 100) {
            $valid_issues += $issue.html_url
            Write-Host "FOUND MATCH: $($issue.html_url) (Stars: $($repo_info.stargazers_count))"
            
            # Post the comment to request assignment
            Write-Host "Posting assignment request..."
            gh issue comment $issue.html_url -b "Hi! I would love to work on this issue. Could you please assign it to me? Thank you!"
            $repo_counts[$repo_path]++
        }
    } catch {
        # Ignore API errors for a single repo and continue
    }
}
    $page++
}

Write-Host "Total fresh 100+ star issues found and commented on: $($valid_issues.Count)"
