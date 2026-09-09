from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    opportunity_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    location = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=True
    )