# CIOS Database Schemas

## MongoDB (Multi-Tenant Relational Structure)

### Users Collection
- `_id`: ObjectId
- `tenantId`: String (Indexed)
- `email`: String (Unique)
- `role`: Enum [ADMIN, URBAN_PLANNER, RESEARCHER, VIEWER]
- `passwordHash`: String

### Projects Collection
- `_id`: ObjectId
- `tenantId`: String (Indexed)
- `name`: String
- `geometry`: GeoJSON Polygon
- `budget`: Number
- `createdAt`: Timestamp

### Interventions Collection
- `_id`: ObjectId
- `projectId`: ObjectId (Ref)
- `type`: Enum [COOL_ROOF, TREE_PLANTATION, WATER_BODY]
- `cost`: Number
- `temperatureReduction`: Number
- `roi`: Number

## Qdrant (Vector Store)

### Collection: `climate_knowledge`
- `id`: UUID
- `vector`: Float32Array[384]
- `payload`: 
  - `text`: String (Chunked paragraph)
  - `source`: String (e.g., "IPCC Report 2023")
  - `page`: Number
