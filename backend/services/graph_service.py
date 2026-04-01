from neo4j import GraphDatabase
from config.settings import settings

import time

class GraphService:
    def __init__(self):
        self.driver = None
        self._initialize_driver()

    def _initialize_driver(self):
        for i in range(5):
            try:
                self.driver = GraphDatabase.driver(
                    settings.neo4j_uri, 
                    auth=(settings.neo4j_user, settings.neo4j_password)
                )
                self.driver.verify_connectivity()
                break
            except Exception as e:
                print(f"Waiting for Neo4j... (Attempt {i+1}/5) | {e}")
                time.sleep(5)

    def close(self):
        self.driver.close()

    def add_project(self, project_id: str, name: str, technologies: list):
        query = """
        MERGE (p:Project {id: $id})
        SET p.name = $name
        WITH p
        UNWIND $technologies AS tech
        MERGE (t:Technology {name: toLower(tech)})
        MERGE (p)-[:USES]->(t)
        """
        try:
            with self.driver.session() as session:
                session.run(query, id=project_id, name=name, technologies=technologies)
        except Exception as e:
            print(f"Neo4j add_project error: {e}")

    def add_paper(self, paper_id: str, title: str):
        query = """
        MERGE (p:Paper {id: $id})
        SET p.title = $title
        """
        try:
            with self.driver.session() as session:
                session.run(query, id=paper_id, title=title)
        except Exception as e:
            print(f"Neo4j add_paper error: {e}")

    def get_related_nodes(self, node_id: str, limit: int = 50):
        query = """
        MATCH (n {id: $id})-[:USES|IMPLEMENTS|RELATED_TO*1..2]-(related)
        RETURN related.id AS r_id, labels(related) AS r_type, related.name AS r_name
        LIMIT $limit
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, id=node_id, limit=limit)
                return [{"id": record["r_id"], "type": record["r_type"][0]} for record in result]
        except Exception as e:
            print(f"Neo4j get_related_nodes error: {e}")
            return []

graph_service = GraphService()
