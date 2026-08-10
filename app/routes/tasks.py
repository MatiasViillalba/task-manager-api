from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Title, description, status, priority and due date for the task.
        current_user: The authenticated user, injected from the JWT token.
        db: Active database session.

    Returns:
        The newly created task.
    """
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=current_user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all tasks belonging to the authenticated user.

    Args:
        status_filter: Optional status value to filter tasks by.
        current_user: The authenticated user, injected from the JWT token.
        db: Active database session.

    Returns:
        A list of tasks owned by the authenticated user.
    """
    query = db.query(Task).filter(Task.user_id == current_user.id)

    if status_filter:
        query = query.filter(Task.status == status_filter)

    return query.all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a single task by its ID.

    Args:
        task_id: The identifier of the task to retrieve.
        current_user: The authenticated user, injected from the JWT token.
        db: Active database session.

    Returns:
        The requested task.

    Raises:
        HTTPException: If the task does not exist or does not belong to the user.
    """
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task
