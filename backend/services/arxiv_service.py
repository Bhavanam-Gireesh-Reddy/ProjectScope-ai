import requests
import xml.etree.ElementTree as ET
import re
import time

def fetch_arxiv_papers(query: str, limit: int = 15):
    """
    Fetches research papers from ArXiv API with robust error handling and query strategies.
    
    ArXiv API docs: https://arxiv.org/help/api/user-manual
    """
    # Clean the query: ArXiv doesn't like special characters except specific boolean operators
    # We'll treat spaces as implicit AND if we don't provide boolean operators
    clean_query = query.replace('"', '').strip()
    
    # Construction of ArXiv search query:
    # We use 'all' field which covers title, abstract, and authors.
    # For multi-word queries, we wrap in quotes for phrase matching or join with AND
    if " " in clean_query and " AND " not in clean_query and " OR " not in clean_query:
        # Strategy: Use phrase matching for short queries, otherwise just the raw string
        search_query = f'all:"{clean_query}"'
    else:
        search_query = f'all:{clean_query}'

    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/xml"
    }

    print(f"ArXiv: Searching for '{search_query}' (Original: '{query}')")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        xml_data = response.content
        root = ET.fromstring(xml_data)
        
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        
        for entry in root.findall("atom:entry", namespace):
            try:
                title_el = entry.find("atom:title", namespace)
                summary_el = entry.find("atom:summary", namespace)
                published_el = entry.find("atom:published", namespace)
                id_el = entry.find("atom:id", namespace)

                if title_el is None or summary_el is None:
                    continue

                title = title_el.text or ""
                abstract = summary_el.text or ""
                published = published_el.text or "2024-01-01"
                link = id_el.text or ""
                
                # Extract authors
                authors = []
                for author in entry.findall("atom:author", namespace):
                    name_el = author.find("atom:name", namespace)
                    if name_el is not None and name_el.text:
                        authors.append(name_el.text.strip())

                # Clean text (remove newlines/bloat)
                clean_title = re.sub(r'\s+', ' ', title).strip()
                clean_abstract = re.sub(r'\s+', ' ', abstract).strip()
                
                papers.append({
                    "id": link.split("/")[-1],
                    "title": clean_title,
                    "abstract": clean_abstract,
                    "year": int(published.split('-')[0]),
                    "authors": authors,
                    "url": link,
                    "citations": 0  # ArXiv doesn't provide citations directly via API
                })
            except Exception as entry_e:
                print(f"ArXiv: Error parsing entry: {entry_e}")
                continue
                
        print(f"ArXiv: Found {len(papers)} papers.")
        
        # Fallback: If no results for a phrase, try without quotes
        if len(papers) == 0 and 'all:"' in search_query:
            print("ArXiv: Retrying with relaxed query...")
            return fetch_arxiv_papers(clean_query.replace('"', ''), limit)
            
        return papers

    except requests.exceptions.RequestException as e:
        print(f"ArXiv Network Error: {e}")
    except Exception as e:
        print(f"ArXiv Unexpected Error: {type(e).__name__}: {e}")
        
    return []
