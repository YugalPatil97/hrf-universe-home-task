from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from home_task.models import DaysToHireStats
from home_task.db import SessionLocal

app = FastAPI()

@app.get("/stats")
def get_latest_stats():
    with SessionLocal() as session:
        latest_stats = (session.query(DaysToHireStats).order_by(DaysToHireStats.id.desc()).first())

        if not latest_stats:
            raise HTTPException(status_code=404, detail="No statistics found.")

        return {"mean": latest_stats.mean,"median": latest_stats.median,"min": latest_stats.min,"max": latest_stats.max,}
