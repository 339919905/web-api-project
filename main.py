"""
Main application entry point for the Task Management API.
This file creates the FastAPI app instance, configures middleware,
registers exception handlers, creates database tables, and mounts routes.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine
from routers.items import router as tasks_router

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Task Management API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description=(
        "A coursework-ready CRUD Web API for managing tasks using FastAPI, "
        "SQLAlchemy, and SQLite."
    ),
)

# Allow local frontend tools or API clients to access the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Return a consistent JSON format for HTTP errors.

    Args:
        request: Incoming request object.
        exc: Raised HTTP exception.

    Returns:
        JSONResponse: Standardized error payload.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP error",
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Return a consistent JSON format for request validation errors.

    Args:
        request: Incoming request object.
        exc: Raised validation exception.

    Returns:
        JSONResponse: Standardized validation error payload.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "detail": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "path": str(request.url.path),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Return a consistent JSON format for unexpected server errors.

    Args:
        request: Incoming request object.
        exc: Unexpected exception instance.

    Returns:
        JSONResponse: Standardized internal server error payload.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "path": str(request.url.path),
        },
    )


# Create database tables when the application starts.
Base.metadata.create_all(bind=engine)

# Register task-related endpoints under /api/tasks.
app.include_router(tasks_router)


@app.get("/", status_code=200)
def read_root():
    """
    Health-check style root endpoint.

    Returns:
        dict: Basic application information.
    """
    return {
        "message": "Task Management API is running.",
        "docs": "/docs",
        "redoc": "/redoc",
        "resource": "tasks",
        "features": [
            "CRUD",
            "pagination",
            "search",
            "filtering",
            "patch",
            "timestamps",
            "standardized-errors",
        ],
    }
