from elasticsearch import Elasticsearch
from config.settings import settings

import time

class IndexingService:
    def __init__(self):
        self.es = Elasticsearch(settings.elasticsearch_host)
        self.index_name = "projectscope_docs"
        # Delay to allow ES to be fully ready
        self._initialize_service()

    def _initialize_service(self):
        for i in range(5):
            try:
                self._create_index()
                break
            except Exception as e:
                print(f"Waiting for Elasticsearch... (Attempt {i+1}/5)")
                time.sleep(5)

    def _create_index(self):
        try:
            if not self.es.indices.exists(index=self.index_name):
                mapping = {
                    "mappings": {
                        "properties": {
                            "doc_type": {"type": "keyword"},
                            "title": {"type": "text"},
                            "description": {"type": "text"},
                            "url": {"type": "keyword"},
                            "stars": {"type": "integer"},
                            "authors": {"type": "keyword"},
                            "year": {"type": "integer"},
                            "citations": {"type": "integer"},
                            "downloads": {"type": "integer"}
                        }
                    }
                }
                self.es.indices.create(index=self.index_name, body=mapping)
                print(f"Created index {self.index_name}")
        except Exception as e:
            print(f"Elasticsearch index creation failed: {e}")

    def index_document(self, doc_id: str, doc_type: str, data: dict):
        try:
            data["doc_type"] = doc_type
            self.es.index(index=self.index_name, id=doc_id, document=data)
        except Exception as e:
            print(f"Elasticsearch indexing failed: {e}")

    def search(self, query: str, limit: int = 20):
        try:
            search_body = {
                "size": limit,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "description^2", "authors"],
                        "fuzziness": "AUTO"
                    }
                }
            }
            res = self.es.search(index=self.index_name, body=search_body)
            results = []
            for hit in res['hits']['hits']:
                item = hit['_source']
                item['id'] = hit['_id']
                results.append(item)
            return results
        except Exception as e:
            print(f"Elasticsearch search failed: {e}")
            return []

indexing_service = IndexingService()
