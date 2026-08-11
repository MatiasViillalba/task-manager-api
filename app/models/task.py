from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class TaskStatus(str, PyEnum):
    """
    Enumeration of task status values.

    PENDING: Task is waiting to be started.
    IN_PROGRESS: Task is currently being worked on.
    COMPLETED: Task has been finished.
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, PyEnum):
    """
    Enumeration of task priority levels.

    LOW: Low priority task.
    MEDIUM: Medium priority task.
    HIGH: High priority task.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    """
    Task model representing a user's task/todo item.

    Attributes:
        id: Unique identifier for the task.
        title: Title of the task.
        description: Detailed description of the task.
        status: Current status of the task (pending, in_progress, completed).
        priority: Priority level of the task (low, medium, high).
        due_date: Optional deadline for the task.
        user_id: Foreign key referencing the owner user.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last modified.
        owner: Relationship to the User model.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True
    )
    priority = Column(
        Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False, index=True
    )
    due_date = Column(DateTime, nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    owner = relationship("User", back_populates="tasks")
