import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import subprocess
import json
import logging

app = FastAPI()

class AnalysisRequest(BaseModel):
    projectId: str
    city: str
    bbox: str

@app.post("/analyze")
async def analyze_city(request: AnalysisRequest, background_tasks: BackgroundTasks):
    def run_analysis_task(req: AnalysisRequest):
        # We would ideally dynamically set the TARGET_CITY and BBOX in config.py
        # For now, we will run the pipeline as a subprocess
        try:
            logging.info(f"Running pipeline for project {req.projectId}")
            # Ensure the current working directory is the root
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            result = subprocess.run(["python", "run_pipeline.py"], cwd=root_dir, capture_output=True, text=True)
            logging.info(f"Pipeline finished with code {result.returncode}")
            
            # Here we would normally parse outputs/hotspot_results.json and update MongoDB
            # For simplicity in this scaffold, we just assume success.
        except Exception as e:
            logging.error(f"Pipeline error: {e}")

    background_tasks.add_task(run_analysis_task, request)
    return {"message": "Analysis started", "projectId": request.projectId}
