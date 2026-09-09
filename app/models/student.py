from sqlalchemy import Column, Integer, String, Float, Date

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        unique=True,
        index=True
    )

    college = Column(
        String,
        nullable=True
    )

    degree = Column(
        String,
        nullable=True
    )

    branch = Column(
        String,
        nullable=True
    )

    graduation_year = Column(
        Integer,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    date_of_birth = Column(
        Date,
        nullable=True
    )

    location = Column(
        String,
        nullable=True
    )

    semester = Column(
        Integer,
        nullable=True
    )

    cgpa = Column(
        Float,
        nullable=True
    )

    preferred_roles = Column(
        String,
        nullable=True
    )

    preferred_industries = Column(
        String,
        nullable=True
    )

    preferred_work_locations = Column(
        String,
        nullable=True
    )

    profile_picture_url = Column(
        String,
        nullable=True
    )

    resume_url = Column(
        String,
        nullable=True
    )