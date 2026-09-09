from sqlalchemy import Column, Integer, String

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    industry = Column(
        String,
        nullable=True
    )

    location = Column(
        String,
        nullable=True
    )

    website = Column(
        String,
        nullable=True
    )