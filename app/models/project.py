from sqlalchemy import Column, Integer, String

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )