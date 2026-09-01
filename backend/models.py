from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    exercise = Column(String, index=True, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow, nullable=False)
