from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    result_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    assessment_id = Column(
        String,
        nullable=False,
        index=True
    )

    overall_score = Column(
        Float,
        nullable=False
    )

    technical_score = Column(
        Float,
        nullable=False
    )

    aptitude_score = Column(
        Float,
        nullable=False
    )

    communication_score = Column(
        Float,
        nullable=False
    )

    problem_solving_score = Column(
        Float,
        nullable=False
    )

    completed_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )