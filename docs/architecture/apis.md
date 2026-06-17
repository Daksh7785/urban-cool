# CIOS API Contracts

## Node.js Gateway APIs
`POST /api/auth/login`
- Body: `{ email, password }`
- Returns: `{ jwt_token, tenantId }`

`POST /api/projects/:tenantId/optimize`
- Auth: Bearer Token required.
- Body: `{ geojson_bounds, budget, objective: "max_cooling" }`
- Returns: `{ jobId: "bullmq-123", status: "queued" }`

## Python Analytics APIs (Internal Microservice)
`POST /internal/ml/forecast`
- Body: `{ city_id, horizon_days: 7 }`
- Returns: `{ risk_matrix, confidence_score }`

`POST /internal/rag/query`
- Body: `{ query: "Explain cool roofs", top_k: 3 }`
- Returns: `{ answer, sources: [] }`
