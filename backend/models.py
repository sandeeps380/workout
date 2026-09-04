from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)
    day = Column(Integer, nullable=False)  # 0=Push, 1=Pull, 3=Legs, 4=Full body
    exercise_index = Column(Integer, nullable=False)  # 0 to 5
    exercise_name = Column(String, nullable=False)
    kg = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return (
            f"<WorkoutLog(id={self.id}, date={self.date!r}, day={self.day}, "
            f"exercise_index={self.exercise_index}, exercise_name={self.exercise_name!r}, "
            f"kg={self.kg})>"
        )
