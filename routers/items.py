"""
Task API routes for the Task Management API.
This file defines CRUD endpoints, pagination support, filtering,
partial updates, and consistent JSON responses with proper HTTP status codes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Task, get_db
from schemas import (
    MessageResponse,
    TaskCreate,
    TaskListResponse,
    TaskPatch,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
def get_tasks(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    search: str | None = Query(default=None, description="Optional title search keyword"),
    completed: bool | None = Query(default=None, description="Optional completion status filter"),
    db: Session = Depends(get_db),
):
    """
    Get a paginated list of tasks with optional filtering.

    Args:
        page: Current page number, starting from 1.
        limit: Maximum number of tasks to return.
        search: Optional title search keyword.
        completed: Optional boolean filter for completion status.
        db: Active database session.

    Returns:
        TaskListResponse: Pagination metadata and task records.
    """
    query = db.query(Task)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    if completed is not None:
        query = query.filter(Task.completed == completed)

    total = query.with_entities(func.count(Task.id)).scalar() or 0
    offset = (page - 1) * limit
    tasks = query.order_by(Task.id.asc()).offset(offset).limit(limit).all()

    return TaskListResponse(page=page, limit=limit, total=total, items=tasks)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a single task by its ID.

    Args:
        task_id: Unique ID of the task.
        db: Active database session.

    Returns:
        TaskResponse: The requested task record.

    Raises:
        HTTPException: If the task does not exist.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Args:
        task: Validated task payload from the request body.
        db: Active database session.

    Returns:
        TaskResponse: The newly created task.
    """
    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Replace an existing task by ID.

    Args:
        task_id: Unique ID of the task to update.
        task_update: Validated replacement data.
        db: Active database session.

    Returns:
        TaskResponse: The updated task record.

    Raises:
        HTTPException: If the task does not exist.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    for field, value in task_update.model_dump().items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def patch_task(task_id: int, task_patch: TaskPatch, db: Session = Depends(get_db)):
    """
    Partially update one or more fields of a task.

    Args:
        task_id: Unique ID of the task to update.
        task_patch: Partial validated update data.
        db: Active database session.

    Returns:
        TaskResponse: The updated task record.

    Raises:
        HTTPException: If the task does not exist.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = task_patch.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.

    Args:
        task_id: Unique ID of the task to delete.
        db: Active database session.

    Returns:
        MessageResponse: Confirmation message in JSON format.

    Raises:
        HTTPException: If the task does not exist.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return MessageResponse(message=f"Task {task_id} deleted successfully")
