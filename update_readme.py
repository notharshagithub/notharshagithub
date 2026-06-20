import json
import os
import re
import urllib.request
from datetime import datetime

USER = "notharshagithub"
HEADERS = {"User-Agent": "notharshagithub-profile-updater"}

token = os.environ.get("GITHUB_TOKEN")
if token:
    HEADERS["Authorization"] = f"token {token}"

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def generate_desc_from_name(name):
    lookup = {
        "BrowseIQ": "Intelligent web parsing, semantic extraction, and DOM analysis library.",
        "Browser-AI-Agent": "Autonomous LLM-driven browser agent for executing automated web workflows.",
        "AETHER": "Advanced lightweight system environment and core shell customization utility.",
        "Portfolio-new": "Modern developer portfolio web app demonstrating full-stack engineering capability.",
        "notharshagithub": "Monochrome configurations and automation pipelines for my GitHub profile."
    }
    if name in lookup:
        return lookup[name]
    clean_name = name.replace("-", " ").replace("_", " ")
    return f"A software development repository for {clean_name.strip()}."

def get_recent_repos():
    url = f"https://api.github.com/users/{USER}/repos?sort=updated&per_page=10"
    repos = fetch_json(url)
    if not repos:
        return ""
    
    non_forks = [r for r in repos if not r.get("fork")][:5]
    if not non_forks:
        non_forks = repos[:5]
        
    lines = ["#### 📁 Recently Updated Repositories\n"]
    for repo in non_forks:
        name = repo["name"]
        url = repo["html_url"]
        desc = repo["description"] or generate_desc_from_name(name)
        stars = repo["stargazers_count"]
        lang = repo["language"] or "Misc"
        
        updated_at = repo["updated_at"]
        try:
            dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
            updated_str = dt.strftime("%b %d, %Y")
        except Exception:
            updated_str = updated_at[:10]
            
        stars_str = f" • ⭐ {stars}" if stars > 0 else ""
        lines.append(f"- 🔗 **[{name}]({url})** — *{lang}*{stars_str} • Updated {updated_str}<br/>\n  _{desc}_")
    
    return "\n".join(lines)

def get_recent_activity():
    url = f"https://api.github.com/users/{USER}/events/public?per_page=20"
    events = fetch_json(url)
    if not events:
        return ""
    
    lines = ["#### ⚡ Recent Activity\n"]
    count = 0
    seen_commits = set()
    
    for event in events:
        if count >= 5:
            break
        
        event_type = event["type"]
        repo_name = event["repo"]["name"]
        repo_url = f"https://github.com/{repo_name}"
        created_at = event["created_at"]
        try:
            dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            date_str = dt.strftime("%b %d, %Y")
        except Exception:
            date_str = created_at[:10]
        
        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            for c in commits:
                if count >= 5:
                    break
                message = c["message"].split("\n")[0]
                if message in seen_commits:
                    continue
                seen_commits.add(message)
                lines.append(f"- 🛠️ Push to **[{repo_name}]({repo_url})**: `{message}` ({date_str})")
                count += 1
        elif event_type == "PullRequestEvent":
            action = event["payload"]["action"]
            pr_title = event["payload"]["pull_request"]["title"]
            pr_url = event["payload"]["pull_request"]["html_url"]
            lines.append(f"- 🔀 Pull Request {action} in **[{repo_name}]({repo_url})**: [{pr_title}]({pr_url}) ({date_str})")
            count += 1
        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            issue_title = event["payload"]["issue"]["title"]
            issue_url = event["payload"]["issue"]["html_url"]
            lines.append(f"- ⚠️ Issue {action} in **[{repo_name}]({repo_url})**: [{issue_title}]({issue_url}) ({date_str})")
            count += 1
            
    if count == 0:
        lines.append("- No recent public events recorded.")
        
    return "\n".join(lines)

def main():
    print("Fetching updated repositories...")
    repos_md = get_recent_repos()
    
    print("Fetching public events activity...")
    activity_md = get_recent_activity()
    
    feed_content = f"\n{repos_md}\n\n{activity_md}\n"
    
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    pattern = r"<!-- START_ACTIVITY -->.*?<!-- END_ACTIVITY -->"
    replacement = f"<!-- START_ACTIVITY -->\n{feed_content}\n<!-- END_ACTIVITY -->"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
