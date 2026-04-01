from groq import Groq
from config.settings import settings
import json

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client

def rerank_and_reason(user_query: str, results: list) -> dict:
    client = get_client()
    if not settings.groq_api_key:
        return {"insights": "No insights available (Groq Key missing).", "roadmap": ["Deploy locally"], "confidence_score": 0.5, "top_results": results[:10]}
        
    prompt = f"""
    Given the user query: "{user_query}"
    And the following top candidate search results (repositories, datasets, and papers):
    {json.dumps(results[:30])}
    
    Task:
    1. Re-rank these results to find the most relevant items.
    2. Provide 2-3 sentences of insights or 'Research Gap' detection based on the available technologies.
    3. Suggest an elaborate 5-6 step roadmap to build this project. Each step should be one detailed sentence describing technical milestones.
    4. Provide a confidence score (0.0 to 1.0) on how feasible the project is based on existing work.
    
    Return pure JSON with:
    - "insights": "..."
    - "roadmap": ["Detailed Step 1...", "Detailed Step 2...", "..."]
    - "confidence_score": 0.85
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a software architect AI."}, {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.choices[0].message.content)
        data["top_results"] = results[:10]
        return data
    except Exception as e:
        print(f"Reranking Error: {e}")
        return {"insights": "Error generating insights.", "roadmap": ["Analyze requirements"], "confidence_score": 0.5, "top_results": results[:10]}
