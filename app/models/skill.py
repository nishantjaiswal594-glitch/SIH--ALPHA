from sqlalchemy import Column, Integer, String

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    skill_name = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=True
    )