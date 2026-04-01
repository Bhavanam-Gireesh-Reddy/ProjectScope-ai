import requests
import urllib.parse
from config.settings import settings

def fetch_github_repos(query: str, limit: int = 10):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if settings.github_token:
        headers["Authorization"] = f"token {settings.github_token}"
    else:
        print("GitHub Warning: No token set. Rate limits will be very low (60 req/hr).")

    # URL-encode the query so multi-word queries work correctly
    # Use quote_plus for GitHub API (replaces spaces with +)
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page={limit}"
    print(f"GitHub: Searching {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            print(f"GitHub: Found {len(items)} repositories for '{query}'")
            repos = []
            for item in items:
                techs = [item.get("language")] if item.get("language") else []
                repos.append({
                    "id": str(item["id"]),
                    "name": item["full_name"],
                    "description": item.get("description"),
                    "url": item["html_url"],
                    "stars": item["stargazers_count"],
                    "technologies": techs
                })
            return repos
        # Log the full error response so we can see exactly what GitHub says
        print(f"GitHub API Error: HTTP {response.status_code} | URL: {url}")
        try:
            print(f"GitHub API Response: {response.json()}")
        except Exception:
            print(f"GitHub API Raw Response: {response.text[:500]}")
    except requests.exceptions.Timeout:
        print("GitHub API Error: Request timed out after 15 seconds")
    except Exception as e:
        print(f"GitHub API Request failed: {e}")
    return []
