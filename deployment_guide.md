# "Free Forever" Deployment Guide

Follow this guide to deploy your **ProjectScope AI** application for $0 lifetime cost.

---

## 1. Setup Your Free Databases
Create accounts and get your connection details for the following services:

| Service | Provider | Free Tier | Action |
| :--- | :--- | :--- | :--- |
| **MongoDB** | [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) | M0 Sandbox (512MB) | Create a "Shared Cluster" and get your `MONGODB_URI`. |
| **Neo4j** | [Neo4j Aura](https://neo4j.com/cloud/aura/) | AuraDB Free | Create a free instance and download the credentials (URI, User, Password). |
| **Redis** | [Upstash](https://upstash.com/) | 10k requests/day | Create a Redis database and get your `REDIS_URL`. |
| **Elasticsearch** | [Bonsai.io](https://bonsai.io/) | Sandbox | Create a free cluster and get the "Access URL" (includes user/pass). |

---

## 2. Deploy Backend (Render)
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` I created.
5. In the **Environment Variables** section, manually add the secret keys you got from Step 1:
   - `MONGODB_URI`
   - `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
   - `REDIS_URL`
   - `ELASTICSEARCH_HOST`
   - `GITHUB_TOKEN`, `GROQ_API_KEY`, `TAVILY_API_KEY`
6. Click **Deploy**. Note down the URL of your backend (e.g., `https://projectscope-backend.onrender.com`).

---

## 3. Deploy Frontend (Vercel)
1. Go to [Vercel](https://vercel.com/new).
2. Import your GitHub repository.
3. Vercel will detect it as a **Vite** project.
4. Under **Environment Variables**, add:
   - `VITE_API_URL`: Paste your **Backend URL** from Step 2.
5. Click **Deploy**.

---

## 4. Updates & Maintenance
- **GitHub Sync**: Every time you `git push` to your repository, both Render and Vercel will automatically redeploy with your latest code.
- **Cold Starts**: On the Render free tier, the backend will "sleep" after 15 minutes of inactivity. The first request after a sleep may take 30-50 seconds to respond. This is normal for free hosting.
