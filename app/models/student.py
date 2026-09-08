from sqlalchemy import Column, Integer, String

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