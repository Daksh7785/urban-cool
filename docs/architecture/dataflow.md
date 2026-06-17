# CIOS Data Flow Diagram

## 1. Asynchronous ML Flow (Optimization & Forecasting)
```text
[React UI] --(POST /api/analyze)--> [Node Express API]
[Node Express API] --(Validate JWT)--> [MongoDB Auth Check]
[Node Express API] --(Push Job)--> [Redis / BullMQ Queue]
[Redis Queue] --(Consume)--> [Python FastAPI Worker]
[Python Worker] --(Pull Earth Engine Data)--> [Google API]
[Python Worker] --(Run XGBoost/NSGA-II)--> [Compute Cluster]
[Python Worker] --(Emit Result)--> [Socket.IO Server]
[Socket.IO Server] --(WSS Event)--> [React UI (Progress Bar 100%)]
```

## 2. Synchronous RAG Flow (Copilot)
```text
[React UI] --(POST /api/chat)--> [Python FastAPI Copilot Route]
[FastAPI] --(Embed Query)--> [SentenceTransformers]
[FastAPI] --(Vector Search)--> [Qdrant Cluster]
[Qdrant] --(Return Chunks)--> [FastAPI]
[FastAPI] --(Construct Context)--> [OpenAI / Local LLM]
[LLM] --(Return Answer)--> [React UI]
```
