# UrbanOS Database Schema

The database utilizes MongoDB with the following heavily-relational collections:

1. **Users**
   - `_id`, `email`, `passwordHash`, `role`, `createdAt`

2. **Projects**
   - `_id`, `userId` (Ref: Users), `name`, `city`, `bounds` (GeoJSON), `createdAt`

3. **Analysis_Jobs**
   - `_id`, `projectId` (Ref: Projects), `status` (queued, running, completed, failed), `type`

4. **Hotspots**
   - `_id`, `projectId` (Ref: Projects), `geometry` (GeoJSON), `mean_lst`, `severity`, `top_drivers` (Array)

5. **Optimization_Results**
   - `_id`, `projectId` (Ref: Projects), `plans` (Array: max_cooling, balanced, max_roi)

6. **Reports**
   - `_id`, `projectId` (Ref: Projects), `filePath`, `generatedAt`

7. **Audit_Logs**
   - `_id`, `userId` (Ref: Users), `action`, `timestamp`, `ip`
