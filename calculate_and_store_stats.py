import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from home_task.models import Base, JobPosting, DaysToHireStats
from home_task.db import engine
import statistics


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/home_task")

engine = create_engine(DATABASE_URL)

def calculate_stats():
    with Session(engine) as session:
        result = session.execute(select(JobPosting.days_to_hire).where(JobPosting.days_to_hire != None))
        days_list = [row[0] for row in result]

        if not days_list:
            print("No valid 'days_to_hire' values found.")
            return

        mean_val = statistics.mean(days_list)
        median_val = statistics.median(days_list)
        min_val = min(days_list)
        max_val = max(days_list)

        print(f"Calculated stats - mean: {mean_val}, median: {median_val}, min: {min_val}, max: {max_val}")

        stats = DaysToHireStats(mean=mean_val,median=median_val,min=min_val,max=max_val)
        session.add(stats)
        session.commit()
        print("Statistics saved to days_to_hire_stats table.")

if __name__ == "__main__":
    calculate_stats()
