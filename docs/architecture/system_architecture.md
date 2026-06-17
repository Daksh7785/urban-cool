# UrbanOS System Architecture

## Overview
UrbanOS is a global climate intelligence platform built on a deeply integrated, event-driven microservices architecture. No service operates independently.

## Components
1. **Frontend (React/Vite/Tailwind):** The client-facing dashboard and GIS workspace.
   - **Inputs:** User interactions, WebSockets events.
   - **Outputs:** REST API calls, rendered UI.
   - **Dependencies:** React, Leaflet, Axios, Socket.IO Client.

2. **Backend API Gateway (Node.js/Express):** The central nervous system.
   - **Inputs:** REST API requests from Frontend, Job Results from Analytics.
   - **Outputs:** Database queries, Redis Queue dispatches, WebSocket broadcasts.
   - **Dependencies:** Express, Mongoose, BullMQ, Socket.IO Server.

3. **Analytics Engine (Python/FastAPI):** Heavy ML computation and physics simulation.
   - **Inputs:** Redis Job Queue items.
   - **Outputs:** Analytics results POSTed back to Backend, Reports saved to File Storage.
   - **Dependencies:** XGBoost, GeoPandas, ReportLab.

4. **Database (MongoDB):** Persistent storage of all state.
   - **Inputs:** Queries from Backend.
   - **Outputs:** JSON documents.

5. **Message Broker (Redis):** Asynchronous task orchestration.
   - **Inputs:** Jobs pushed from Backend.
   - **Outputs:** Jobs popped by Python workers.
