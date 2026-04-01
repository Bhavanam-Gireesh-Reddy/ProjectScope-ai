import motor.motor_asyncio
from config.settings import settings
import datetime

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_uri)
db = client.projectscope
searches_collection = db.get_collection("searches")

async def save_search(query: str, results: dict):
    """
    Persist a search query and its AI generated insights/results to MongoDB.
    """
    document = {
        "query": query,
        "timestamp": datetime.datetime.utcnow(),
        "insights": results.get("insights"),
        "roadmap": results.get("roadmap"),
        "confidence_score": results.get("confidence_score", 0),
        "total_results": len(results.get("repositories", [])) + len(results.get("papers", [])) + len(results.get("datasets", []))
    }
    
    try:
        await searches_collection.insert_one(document)
    except Exception as e:
        print(f"MongoDB Insert Error: {e}")

async def get_recent_searches(limit: int = 50):
    """
    Fetch historical searches chronologically.
    """
    cursor = searches_collection.find().sort("timestamp", -1).limit(limit)
    documents = await cursor.to_list(length=limit)
    
    history = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string for JSON serialization
        history.append(doc)
    
    return history
