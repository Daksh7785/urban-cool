# CIOS Master Architecture Diagram

## 1. Top-Level Ecosystem
```mermaid
graph TD
    A[React Frontend] -->|HTTPS REST| B(Node.js API Gateway)
    A -->|WebSockets WSS| B
    B -->|Mongoose ODM| C[(MongoDB Cluster)]
    B -->|Push Job| D[[Redis BullMQ Queue]]
    D -->|Consume Job| E{Python Analytics Worker}
    E -->|Fetch LST Data| F[Google Earth Engine]
    E -->|NSGA-II / XGBoost| G[Local Compute]
    E -->|Emit Progress| B
```

## 2. RAG Copilot Architecture
```mermaid
graph TD
    A[React UI] -->|Query| B[FastAPI ML Service]
    B -->|Embed Text| C[SentenceTransformers]
    C -->|Vector Search| D[(Qdrant Vector DB)]
    D -->|Top 3 Chunks| B
    B -->|Synthesize| E[LLM Engine]
```

## 3. Structural Integrity Report
- **Frontend ↔ Backend:** Connected. React `App.tsx` routes Axios requests to `localhost:5000/api`.
- **Backend ↔ MongoDB:** Connected. `mongoose.connect()` initialized in Express server with strict `tenantId` schemas.
- **Backend ↔ Analytics:** Connected asynchronously. Express pushes to `Redis`; Python `bullmq_worker.ts` consumes and executes ML jobs.
- **Analytics ↔ Storage:** Connected. XGBoost models save weights to `.pkl`/`.json` locally; Vector chunks persist in Qdrant.
