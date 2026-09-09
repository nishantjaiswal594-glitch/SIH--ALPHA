from sqlalchemy import Column, Integer, String

from app.database import Base


class OpportunitySkill(Base):
    __tablename__ = "opportunity_skills"

    opportunity_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    skill_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    required_level = Column(
        String,
        nullable=True
    )