import requests
import xml.etree.ElementTree as ET
import re
import time
import random

def fetch_arxiv_papers(query: str, limit: int = 15):
    """
    Fetches research papers from ArXiv API with a 3-stage fallback strategy for maximum reliability.
    Includes rate-limit handling and exponential backoff to avoid 429 errors.
    """
    clean_query = re.sub(r'[^\w\s]', '', query).strip()
    if not clean_query:
        return []
        
    words = clean_query.split()
    
    # Strategy 1: Exact Phrase (Most accurate)
    # Strategy 2: All words (AND logic)
    # Strategy 3: Any words (OR logic - relaxed)
    strategies = [
        f'all:"{clean_query}"',
        ' AND '.join([f'all:{w}' for w in words]),
        ' OR '.join([f'all:{w}' for w in words])
    ]
    
    url = "https://export.arxiv.org/api/query"
    # Use a more stable and professional User-Agent
    headers = {
        "User-Agent": "ProjectScopeAI/1.0 (Research Tool; contact: research@projectscope.ai)",
        "Accept": "application/xml"
    }

    for attempt, search_query in enumerate(strategies):
        # ArXiv guidelines suggest 1 request every 3 seconds.
        # We add a small random jitter to avoid synchronized requests.
        if attempt > 0:
            wait_time = 3 + random.uniform(0.5, 1.5)
            print(f"ArXiv: Waiting {wait_time:.1f}s before fallback strategy {attempt+1}...")
            time.sleep(wait_time)

        print(f"ArXiv Attempt {attempt+1}: Querying '{search_query}'")
        params = {
            "search_query": search_query,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        max_retries = 2
        for retry in range(max_retries + 1):
            try:
                # Increased timeout to 30s as ArXiv API can be slow
                response = requests.get(url, params=params, headers=headers, timeout=30)
                
                if response.status_code == 429:
                    # Rate limit exceeded. Wait longer and retry.
                    wait = (retry + 1) * 5 + random.uniform(1, 3)
                    print(f"ArXiv: 429 Rate Limit exceeded. Retrying in {wait:.1f}s...")
                    time.sleep(wait)
                    continue
                    
                if response.status_code == 403:
                    print("ArXiv: 403 Forbidden - IP may be temporarily blocked. Skipping strategy.")
                    break
                    
                response.raise_for_status()
                
                root = ET.fromstring(response.content)
                namespace = {"atom": "http://www.w3.org/2005/Atom"}
                papers = []
                
                for entry in root.findall("atom:entry", namespace):
                    try:
                        title_el = entry.find("atom:title", namespace)
                        summary_el = entry.find("atom:summary", namespace)
                        id_el = entry.find("atom:id", namespace)
                        published_el = entry.find("atom:published", namespace)

                        if title_el is None or title_el.text is None: 
                            continue

                        title = title_el.text.strip()
                        # ArXiv sometimes returns a "Error" entry if the query is invalid
                        if "Error" in title and len(title) < 10:
                            continue

                        abstract = (summary_el.text or "").strip()
                        link = (id_el.text or "").strip()
                        date_text = (published_el.text or "2024").strip()
                        year_match = re.search(r'\d{4}', date_text)
                        year = int(year_match.group()) if year_match else 2024
                        
                        authors = []
                        for author in entry.findall("atom:author", namespace):
                            name_el = author.find("atom:name", namespace)
                            if name_el is not None and name_el.text:
                                authors.append(name_el.text.strip())

                        papers.append({
                            "id": link.split("/")[-1],
                            "title": re.sub(r'\s+', ' ', title),
                            "abstract": re.sub(r'\s+', ' ', abstract),
                            "year": year,
                            "authors": authors,
                            "url": link,
                            "citations": 0
                        })
                    except Exception as e:
                        print(f"ArXiv Parse Entry Error: {e}")
                        continue

                if papers:
                    print(f"ArXiv: Successfully found {len(papers)} papers on attempt {attempt+1}")
                    return papers
                
                print(f"ArXiv: No results for strategy {attempt+1}. Moving to next...")
                break # Break out of retry loop to try next strategy
                
            except requests.exceptions.Timeout:
                print(f"ArXiv: Timeout on attempt {attempt+1}, retry {retry+1}")
                if retry == max_retries:
                    print("ArXiv: Max retries reached for this strategy due to timeout.")
                continue
            except Exception as e:
                print(f"ArXiv Strategy {attempt+1} Error: {e}")
                break

    print("ArXiv: All search strategies failed to return results.")
    return []

