$recent_date = (Get-Date).AddDays(-14).ToString("yyyy-MM-dd")
$query = "is:issue is:open label:`"help wanted`" no:assignee comments:0 created:>$recent_date"
$encoded_query = [uri]::EscapeDataString($query)

$valid_issues = @()
$page = 1

while ($valid_issues.Count -lt 1 -and $page -le 3) {
    Write-Host "Searching page $page for fresh, 0-comment issues created in the last 14 days..."
    $search_url = "/search/issues?q=$encoded_query&sort=created&order=desc&per_page=100&page=$page"
    $issues = gh api $search_url | ConvertFrom-Json
    
    if ($issues.items.Count -eq 0) {
        break
    }

    foreach ($issue in $issues.items) {
        if ($valid_issues.Count -ge 1) {
            break
        }
        
        $repo_url = $issue.repository_url
        $repo_path = $repo_url -replace "https://api.github.com/repos/", ""
        
        try {
            $repo_info = gh api "/repos/$repo_path" | ConvertFrom-Json
            if ($repo_info.stargazers_count -ge 100) {
                $valid_issues += $issue.html_url
                Write-Host "FOUND MATCH: $($issue.html_url) (Stars: $($repo_info.stargazers_count))"
                
                Write-Host "Posting assignment request..."
                gh issue comment $issue.html_url -b "Hi! I would love to work on this issue. /assign me"
            }
        } catch {
        }
    }
    $page++
}

Write-Host "Done!"
