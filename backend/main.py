from typing import List, Optional

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import get_db, init_db

app = FastAPI(title="Workout Tracker")


@app.on_event("startup")
def on_startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkoutCreate(BaseModel):
    exercise: str
    sets: int
    reps: int
    weight: Optional[float] = None


class WorkoutOut(WorkoutCreate):
    id: int

    class Config:
        from_attributes = True


@app.get("/")
def read_root():
    return {"message": "Workout Tracker API"}


@app.get("/workouts", response_model=List[WorkoutOut])
def list_workouts(db: Session = Depends(get_db)):
    return db.query(models.Workout).all()


@app.post("/workouts", response_model=WorkoutOut)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = models.Workout(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout
