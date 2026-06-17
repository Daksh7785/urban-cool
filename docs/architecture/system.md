# CIOS System Architecture

## Component Overview

1. **React Frontend (Vite + TS + Tailwind)**
   - Operates as the UI Command Center. Connects via HTTPS REST and WSS WebSockets.

2. **Node.js API Gateway (Express)**
   - Handles JWT Auth, Tenant Routing, and Rate Limiting.
   - Pushes heavy analytical payloads to BullMQ.

3. **Redis Task Queue (BullMQ)**
   - Orchestrates jobs between the Node Gateway and Python ML engines.

4. **Python Climate Engine (FastAPI + PyTorch/XGBoost)**
   - Consumes jobs from Redis. Runs intensive ETL, Forecasting, and Optimization routines.

5. **MongoDB (Database)**
   - Multi-tenant data store for user profiles, interventions, and project geometries.

6. **Qdrant Vector Database**
   - High-performance vector engine for RAG (Retrieval-Augmented Generation) Copilot operations.
