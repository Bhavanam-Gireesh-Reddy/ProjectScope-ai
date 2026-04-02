from fastapi import APIRouter
from models.schemas import SearchRequest, SearchResponse, Repo, Paper
from services.query_processor import process_query
from services.github_service import fetch_github_repos
from services.kaggle_service import fetch_kaggle_datasets
from services.arxiv_service import fetch_arxiv_papers
from services.indexing_service import indexing_service
from services.graph_service import graph_service
from services.reranker_service import rerank_and_reason
from database import save_search, get_recent_searches

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    # 1. Expand Query with LLM
    query_info = process_query(request.query)
    expanded_query = query_info.get("expanded_query", request.query)
    
    # 2. Fetch external data live for top results (In prod, this is done via background workers)
    # Using dual-query for GitHub/Kaggle to ensure high relevance and stars
    keywords = query_info.get("keywords", [])
    primary_term = " ".join(keywords[:2]) if keywords else request.query
    
    # Run two different searches for better coverage
    repos_1 = fetch_github_repos(request.query, limit=5) # Search user-centric query
    repos_2 = fetch_github_repos(primary_term, limit=10) # Search category-centric query
    
    datasets_1 = fetch_kaggle_datasets(request.query, limit=5)
    datasets_2 = fetch_kaggle_datasets(primary_term, limit=5)
    
    # Merge and Deduplicate (simple set-based dedup by ID)
    def dedup_nodes(list1, list2):
        seen = set()
        merged = []
        for item in (list1 + list2):
            if item["id"] not in seen:
                merged.append(item)
                seen.add(item["id"])
        return merged

    live_repos = dedup_nodes(repos_1, repos_2)
    live_datasets = dedup_nodes(datasets_1, datasets_2)
    live_papers = fetch_arxiv_papers(expanded_query, limit=15)
    
    # Fallback if expanded query returned nothing
    if not live_papers and expanded_query != request.query:
        print(f"ArXiv: Expanded query '{expanded_query}' failed. Falling back to original: '{request.query}'")
        live_papers = fetch_arxiv_papers(request.query, limit=10)
    
    # Optional: Index newly found records into Elasticsearch
    for repo in live_repos:
        indexing_service.index_document(repo["id"], "repo", repo)
        graph_service.add_project(repo["id"], repo["name"], repo.get("technologies", []))
        
    for dataset in live_datasets:
        indexing_service.index_document(dataset["id"], "dataset", dataset)

    # 3. Fast Retrieval from Elasticsearch + Graph expansion
    es_results = indexing_service.search(expanded_query, limit=20)
    graph_expanded = []
    
    # Extremely simplified mock expansion of top hits using Neo4j
    for doc in es_results[:5]:
        related = graph_service.get_related_nodes(doc["id"], limit=5)
        # In a real app we would fetch the related documents fully again
        graph_expanded.extend(related)

    # 4. Merge and Deduplicate
    candidate_results = live_repos + live_datasets + live_papers # In reality: merge ES + Graph + Live
    
    # 5. LLM Re-Ranking and Insight Generation
    reranked = rerank_and_reason(request.query, candidate_results)
    
    # Map back to response models
    final_repos = []
    final_papers = []
    final_datasets = []
    
    from models.schemas import Dataset
    for item in candidate_results:  # Simplified; usually use 'reranked["top_results"]'
        if "stars" in item:
            final_repos.append(Repo(**item))
        elif "downloads" in item:
            final_datasets.append(Dataset(**item))
        elif "authors" in item or "citations" in item or "year" in item:
            final_papers.append(Paper(**{
                "id": str(item.get("id", item.get("title", ""))),
                "title": item.get("title", ""),
                "authors": item.get("authors", []),
                "abstract": item.get("abstract", item.get("description", "")),
                "url": item.get("url", ""),
                "citations": item.get("citations", 0),
                "year": item.get("year", 2024),
                "influential": item.get("influential", False)
            }))

    response_data = {
        "repositories": final_repos,
        "papers": final_papers,
        "datasets": final_datasets,
        "insights": reranked.get("insights", "Standard insights."),
        "roadmap": reranked.get("roadmap", ["Design system", "Implement Core", "Testing"]),
        "confidence_score": reranked.get("confidence_score", 0.8)
    }

    # Save to history database silently
    await save_search(request.query, response_data)

    return SearchResponse(**response_data)

@router.get("/history")
async def get_history():
    history = await get_recent_searches()
    return {"history": history}
