# CIOS API Contracts & Specifications

## Authentication Routes
### `POST /api/auth/login`
**Description:** Authenticates a user and provisions a multi-tenant JWT.
- **Payload:** `{ "email": "user@city.gov", "password": "hash" }`
- **Response (200):** `{ "token": "ey...", "tenantId": "org-indore-123" }`

## Core Analytical Routes
### `POST /api/projects/:tenantId/optimize`
**Description:** Queues a massive Multi-Objective Optimization job (NSGA-II) via BullMQ.
- **Headers:** `Authorization: Bearer <token>`
- **Payload:** 
  ```json
  {
    "geojson_bounds": "Polygon(...)",
    "budget": 5000000,
    "objective": "max_cooling"
  }
  ```
- **Response (202):** `{ "jobId": "bullmq-123", "status": "queued" }`

## Copilot & Inference Routes
### `POST /internal/rag/query`
**Description:** Queries the Qdrant vector database via the Python Copilot microservice.
- **Payload:** `{ "query": "Explain cool roofs", "top_k": 3 }`
- **Response (200):** 
  ```json
  {
    "answer": "Cool roofs increase albedo...",
    "sources": ["IPCC AR6 WGII, Page 45"]
  }
  ```
