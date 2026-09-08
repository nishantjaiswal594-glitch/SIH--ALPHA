from sqlalchemy import Column, Integer, String

from app.database import Base


class StudentSkill(Base):
    __tablename__ = "student_skills"

    student_id = Column(
        Integer,
        primary_key=True
    )

    skill_id = Column(
        Integer,
        primary_key=True
    )

    proficiency_level = Column(
        String,
        nullable=True
    )