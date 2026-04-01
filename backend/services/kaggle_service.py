import requests
from config.settings import settings

def fetch_kaggle_datasets(query: str, limit: int = 5):
    """Fetch matching datasets from Kaggle public API."""
    if not settings.kaggle_username or not settings.kaggle_key:
        print("Kaggle credentials not set. Skipping Kaggle fetching.")
        return []

    url = f"https://www.kaggle.com/api/v1/datasets/list?search={query}"
    
    try:
        response = requests.get(url, auth=(settings.kaggle_username, settings.kaggle_key))
        if response.status_code == 200:
            data = response.json()
            datasets = []
            for item in data[:limit]:
                ref = item.get("ref", "")
                datasets.append({
                    "id": ref,
                    "title": item.get("title", ""),
                    "description": item.get("subtitle") or "",
                    "url": f"https://www.kaggle.com/datasets/{ref}" if ref else "",
                    "downloads": item.get("downloadCount", 0)
                })
            return datasets
        else:
            print(f"Kaggle API returned status code {response.status_code}")
    except Exception as e:
        print(f"Kaggle API Error: {e}")
    return []
