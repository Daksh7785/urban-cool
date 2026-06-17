# UrbanOS API Contracts (OpenAPI Specification Blueprint)

## Core Routes

### Authentication
- `POST /api/auth/login`
  - **Input:** `{ email, password }`
  - **Output:** `{ token, user }`

### Projects
- `POST /api/projects`
  - **Input:** `{ name, city, bounds }`
  - **Output:** `ProjectObject`

### Analysis Workflow
- `POST /api/analysis/start`
  - **Input:** `{ projectId }`
  - **Output:** `{ jobId, status: "queued" }`
  - **Side-effect:** Pushes to Redis Queue.

- `GET /api/analysis/:jobId`
  - **Output:** `{ status, progress, results }`

### GIS Data
- `GET /api/hotspots?projectId={id}`
  - **Output:** `[HotspotObject]`

### Optimization & Reporting
- `POST /api/optimization/run`
  - **Input:** `{ projectId, budget }`
  - **Output:** `{ jobId }`

- `POST /api/report/export`
  - **Input:** `{ projectId }`
  - **Output:** `{ downloadUrl }`
