from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from app.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Attributes:
        title: Title of the task.
        description: Optional detailed description.
        status: Current status, defaults to pending.
        priority: Priority level, defaults to medium.
        due_date: Optional deadline for the task.
    """

    title: str = Field(min_length=1, max_length=255, examples=["Finish project report"])
    description: str | None = Field(
        default=None, examples=["Write the final summary and submit it"]
    )
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = Field(default=None, examples=["2026-12-31T23:59:59"])

    @field_validator("due_date")
    @classmethod
    def due_date_cannot_be_in_the_past(cls, value: datetime | None) -> datetime | None:
        """
        Validate that the due date, if provided, is not in the past.

        Args:
            value: The due date to validate.

        Returns:
            The validated due date.

        Raises:
            ValueError: If the due date is in the past.
        """
        if value is not None:
            comparison_now = datetime.now(timezone.utc)
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            if value < comparison_now:
                raise ValueError("due_date cannot be in the past")
        return value


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields are optional since updates may be partial.

    Attributes:
        title: New title for the task.
        description: New description for the task.
        status: New status for the task.
        priority: New priority for the task.
        due_date: New deadline for the task.
    """

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    """
    Schema for task data returned by the API.

    Attributes:
        id: Unique identifier of the task.
        title: Title of the task.
        description: Detailed description of the task.
        status: Current status of the task.
        priority: Priority level of the task.
        due_date: Deadline for the task, if set.
        user_id: Identifier of the user who owns this task.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last modified.
    """

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
