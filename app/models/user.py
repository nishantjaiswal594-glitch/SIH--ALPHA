from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=True
    )

    role = Column(
        String,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    verification_token_hash = Column(
        String,
        nullable=True
    )

    verification_expires = Column(
        DateTime,
        nullable=True
    )

    reset_token_hash = Column(
        String,
        nullable=True
    )

    reset_token_expires = Column(
        DateTime,
        nullable=True
    )

    google_id = Column(
        String,
        unique=True,
        nullable=True
    )