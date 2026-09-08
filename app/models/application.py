from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    opportunity_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    status = Column(
        String,
        nullable=True
    )

    applied_at = Column(
        DateTime,
        nullable=True
    )