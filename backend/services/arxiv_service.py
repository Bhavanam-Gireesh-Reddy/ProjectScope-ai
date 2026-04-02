import requests
import xml.etree.ElementTree as ET
import re
import time

def fetch_arxiv_papers(query: str, limit: int = 15):
    """
    Fetches research papers from ArXiv API with a 3-stage fallback strategy for maximum reliability.
    """
    clean_query = re.sub(r'[^\w\s]', '', query).strip()
    words = clean_query.split()
    
    # Strategy 1: Exact Phrase (Most accurate)
    strategies = [
        f'all:"{clean_query}"',
        ' AND '.join([f'all:{w}' for w in words]),
        '+'.join(words) # Simple keyword join (Loose)
    ]
    
    url = "https://export.arxiv.org/api/query"
    headers = {
        "User-Agent": f"ProjectScopeAI/1.0 (contact: research@projectscope.ai; bot-id: {int(time.time())})",
        "Accept": "application/xml"
    }

    for attempt, search_query in enumerate(strategies):
        print(f"ArXiv Attempt {attempt+1}: Querying '{search_query}'")
        params = {
            "search_query": search_query,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 403:
                print("ArXiv: 403 Forbidden - Likely IP rate limit or block. Retrying in loose mode...")
                continue
                
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

                    if title_el is None: continue

                    title = (title_el.text or "").strip()
                    abstract = (summary_el.text or "").strip()
                    link = (id_el.text or "").strip()
                    date = (published_el.text or "2024").split("-")[0]
                    
                    authors = []
                    for author in entry.findall("atom:author", namespace):
                        name_el = author.find("atom:name", namespace)
                        if name_el is not None:
                            authors.append(name_el.text.strip())

                    papers.append({
                        "id": link.split("/")[-1],
                        "title": re.sub(r'\s+', ' ', title),
                        "abstract": re.sub(r'\s+', ' ', abstract),
                        "year": int(date) if date.isdigit() else 2024,
                        "authors": authors,
                        "url": link,
                        "citations": 0
                    })
                except Exception as e:
                    print(f"ArXiv Parse Error: {e}")
                    continue

            if papers:
                print(f"ArXiv: Found {len(papers)} papers on attempt {attempt+1}")
                return papers
            
            print(f"ArXiv: No results for attempt {attempt+1}. Trying next strategy...")
            
        except Exception as e:
            print(f"ArXiv Strategy {attempt+1} Error: {e}")
            continue

    print("ArXiv: All search strategies failed. Returning empty list.")
    return []
