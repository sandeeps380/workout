from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import get_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Workout Tracker",
    description="A small API for logging and reviewing workout sets.",
    lifespan=lifespan,
)


class WorkoutLogCreate(BaseModel):
    date: str
    day: int
    exercise_index: int
    exercise_name: str
    kg: float


class WorkoutLogResponse(WorkoutLogCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


@app.post("/log", response_model=WorkoutLogResponse, status_code=201)
def create_log(entry: WorkoutLogCreate, db: Session = Depends(get_db)):
    db_entry = models.WorkoutLog(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.get("/history", response_model=List[WorkoutLogResponse])
def get_history(exercise_name: str, db: Session = Depends(get_db)):
    return (
        db.query(models.WorkoutLog)
        .filter(models.WorkoutLog.exercise_name == exercise_name)
        .order_by(models.WorkoutLog.date.asc())
        .all()
    )


@app.get("/health")
def health():
    return {"status": "ok"}
