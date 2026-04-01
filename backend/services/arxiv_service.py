import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re

def fetch_arxiv_papers(query: str, limit: int = 10):
    query_encoded = urllib.parse.quote(query)
    # Use https:// -- ArXiv requires HTTPS now
    url = f"https://export.arxiv.org/api/query?search_query=all:{query_encoded}&start=0&max_results={limit}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ProjectScopeAI/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", namespace):
            title_el = entry.find("atom:title", namespace)
            summary_el = entry.find("atom:summary", namespace)
            published_el = entry.find("atom:published", namespace)
            id_el = entry.find("atom:id", namespace)

            if title_el is None or summary_el is None or published_el is None or id_el is None:
                continue  # Skip malformed entries

            title = title_el.text or ""
            abstract = summary_el.text or ""
            published = published_el.text or "2000-01-01"
            link = id_el.text or ""
            authors = [author.find("atom:name", namespace).text for author in entry.findall("atom:author", namespace)
                       if author.find("atom:name", namespace) is not None]
            
            papers.append({
                "id": link.split("/")[-1],
                "title": re.sub(r'\s+', ' ', title).strip(),
                "abstract": re.sub(r'\s+', ' ', abstract).strip(),
                "year": int(published.split('-')[0]),
                "authors": authors,
                "url": link,
                "citations": 0  # Citations from ArXiv are not direct
            })
            
        print(f"ArXiv: fetched {len(papers)} papers for query '{query}'")
        return papers
    except urllib.error.URLError as e:
        print(f"ArXiv URL Error: {e.reason} | URL: {url}")
    except urllib.error.HTTPError as e:
        print(f"ArXiv HTTP Error: {e.code} - {e.reason}")
    except Exception as e:
        print(f"ArXiv Error: {type(e).__name__}: {e}")
    return []
