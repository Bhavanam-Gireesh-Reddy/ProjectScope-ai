# ProjectScope AI - Graph-Augmented Project Discovery Engine

## Overview

A system allowing users to describe project ideas in natural language. It retrieves and ranks relevant GitHub repositories, papers, and other resources using Elasticsearch, Neo4j, and LLM-powered reranking.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React + Tailwind CSS (Vite)
- **Search Index**: Elasticsearch
- **Graph DB**: Neo4j
- **Storage**: MongoDB, Redis
- **AI**: Groq (Llama-3.3-70B-Versatile)

## Setup Instructions

1. **Clone the repository** (or navigate to this directory)
2. **Copy the Env file**: `cp .env.example .env`
3. **Fill in API Keys** in the `.env` file (OpenAI, GitHub, etc.)
4. **Run Docker Compose**:

```bash
docker-compose up --build -d
```

5. **Access the application**:

- Frontend: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/docs`
- Elasticsearch: `http://localhost:9200`
- Neo4j Browser: `http://localhost:7474` (Login: neo4j/password123)

## Architecture

- **Step 1**: Query goes to LLM to expand and identify domain.
- **Step 2**: Fast retrieval using Elasticsearch.
- **Step 3**: Neo4j Graph traversal to find related tech and similar nodes.
- **Step 4**: Results are merged, deduplicated, and passed back to LLM for final reasoning/re-ranking.
