# UrbanOS Data Flow

1. **Initiation:** The User creates a Project via the Frontend. The Backend stores the Project in MongoDB.
2. **Job Queueing:** The User clicks "Start Analysis". The Backend generates an `Analysis_Job` document in MongoDB and pushes a task payload to Redis.
3. **Execution:** The Python Analytics Engine listens to Redis, pops the job, and executes the simulation.
4. **Data Persistence:** The Python Engine pushes the completed Hotspot geometries and Optimization JSONs back to the Backend via a secure internal REST endpoint. The Backend saves this into MongoDB.
5. **Real-Time Alert:** The Backend emits a `job_completed` Socket.IO event.
6. **UI Hydration:** The Frontend receives the Socket event and immediately triggers a `GET /api/hotspots` call. The Leaflet map instantly updates with the new data loaded directly from the database.
