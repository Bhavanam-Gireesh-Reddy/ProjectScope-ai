from groq import Groq
from config.settings import settings
import json

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client

def process_query(user_query: str) -> dict:
    client = get_client()
    if not settings.groq_api_key:
        return {"expanded_query": user_query, "domain": "software", "keywords": [user_query]}
        
    prompt = f"""
    Analyze the following user project idea and extract details for search systems:
    Query: "{user_query}"
    
    Return a strictly formatted JSON object with:
    - "expanded_query": A clean, robust academic search query for ArXiv (detailed and specific).
    - "domain": The general field (e.g., AI, Web, DevOps).
    - "keywords": A list of 3-5 broad, high-impact technical keywords for GitHub/Kaggle search (e.g., for "Brain Tumor", keywords should be ["brain tumor", "medical imaging", "deep learning"]).
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a tech search assistant."}, {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Query Processing Error: {e}")
        return {"expanded_query": user_query, "domain": "software", "keywords": [user_query]}
