from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
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


@router.get(
    "",
    response_model=PaginatedResponse[TaskResponse],
    summary="List tasks with pagination and filters",
)
async def get_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    priority_filter: str | None = Query(default=None, alias="priority"),
    due_date_from: datetime | None = Query(default=None),
    due_date_to: datetime | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List tasks belonging to the authenticated user with pagination, sorting and filtering.

    Args:
        status_filter: Optional status value to filter tasks by.
        priority_filter: Optional priority value to filter tasks by.
        due_date_from: Optional lower bound for the due date range.
        due_date_to: Optional upper bound for the due date range.
        limit: Maximum number of tasks to return.
        offset: Number of tasks to skip.
        sort_by: Field to sort by (created_at, updated_at, status, priority).
        sort_order: Sort direction, either asc or desc.
        current_user: The authenticated user, injected from the JWT token.
        db: Active database session.

    Returns:
        A paginated response containing the total count and the list of tasks.
    """
    query = db.query(Task).filter(Task.user_id == current_user.id)

    if status_filter:
        query = query.filter(Task.status == status_filter)

    if priority_filter:
        query = query.filter(Task.priority == priority_filter)

    if due_date_from:
        query = query.filter(Task.due_date >= due_date_from)

    if due_date_to:
        query = query.filter(Task.due_date <= due_date_to)

    total = query.count()

    allowed_sort_fields = {
        "created_at": Task.created_at,
        "updated_at": Task.updated_at,
        "status": Task.status,
        "priority": Task.priority,
        "title": Task.title,
    }
    sort_column = allowed_sort_fields.get(sort_by, Task.created_at)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    tasks = query.limit(limit).offset(offset).all()

    return PaginatedResponse(total=total, limit=limit, offset=offset, items=tasks)


@router.get(
    "/{task_id}", response_model=TaskResponse, summary="Get a single task by ID"
)
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


@router.patch("/{task_id}", response_model=TaskResponse, summary="Update a task")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing task belonging to the authenticated user.

    Args:
        task_id: The identifier of the task to update.
        task_data: Fields to update, all optional for partial updates.
        current_user: The authenticated user, injected from the JWT token.
        db: Active database session.

    Returns:
        The updated task.

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

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task"
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an existing task belonging to the authenticated user.

    Args:
        task_id: The identifier of the task to delete.
        current_user: The authenticated user, injected from the JWT token.
        db: Active database session.

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

    db.delete(task)
    db.commit()
