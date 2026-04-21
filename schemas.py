"""
Pydantic schemas for request validation and JSON responses.
This file defines the input and output shapes used by the API,
including paginated list responses, error payloads, and timestamps.
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Shared task fields used across multiple schemas."""

    title: str = Field(..., min_length=1, max_length=150, description="Task title")
    description: str | None = Field(default=None, description="Detailed task description")
    completed: bool = Field(default=False, description="Task completion status")
    due_date: date | None = Field(default=None, description="Optional due date")


class TaskCreate(TaskBase):
    """Schema used when creating a new task."""


class TaskUpdate(BaseModel):
    """Schema used when replacing an existing task with PUT."""

    title: str = Field(..., min_length=1, max_length=150, description="Updated task title")
    description: str | None = Field(default=None, description="Updated task description")
    completed: bool = Field(..., description="Updated completion status")
    due_date: date | None = Field(default=None, description="Updated due date")


class TaskPatch(BaseModel):
    """Schema used when partially updating a task with PATCH."""

    title: str | None = Field(default=None, min_length=1, max_length=150, description="Updated task title")
    description: str | None = Field(default=None, description="Updated task description")
    completed: bool | None = Field(default=None, description="Updated completion status")
    due_date: date | None = Field(default=None, description="Updated due date")


class TaskResponse(TaskBase):
    """Schema returned for a single task in API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Paginated response returned when listing tasks."""

    page: int
    limit: int
    total: int
    items: list[TaskResponse]


class MessageResponse(BaseModel):
    """Simple response schema for success messages."""

    message: str


class ErrorResponse(BaseModel):
    """Standardized error payload returned by custom exception handlers."""

    error: str
    detail: str | list[dict]
    status_code: int
