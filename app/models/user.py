from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    User model representing a registered user in the system.

    Attributes:
        id: Unique identifier for the user.
        email: User's email address (must be unique).
        hashed_password: Bcrypt hashed password.
        created_at: Timestamp when the user was created.
        tasks: Relationship to all tasks created by this user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
