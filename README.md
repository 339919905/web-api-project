# Task Management API

A coursework-ready Web API project built with **Python + FastAPI + SQLAlchemy + SQLite**.
This application provides a complete CRUD interface for managing tasks, stores data in a SQL database, validates input using Pydantic, and returns structured JSON responses with appropriate HTTP status codes.

## 1. Project Overview

This project was designed to satisfy common university coursework requirements for a backend API assignment:

- Build a Web API that performs full CRUD operations
- Use a relational SQL database for persistent storage
- Implement at least four HTTP endpoints
- Return correct JSON responses
- Use appropriate HTTP status codes
- Make the project runnable locally
- Provide documentation and testing evidence

### Resource Chosen

The project uses a **Task** resource.

Each task contains the following fields:

- `id` - integer primary key
- `title` - task title
- `description` - optional description text
- `completed` - boolean status indicating whether the task is finished
- `due_date` - optional due date in `YYYY-MM-DD` format
- `created_at` - timestamp when the task was created
- `updated_at` - timestamp when the task was last updated

## 2. Technology Stack

This project uses the following stack:

- **Python** - programming language
- **FastAPI** - web framework
- **SQLAlchemy** - ORM for database interaction
- **SQLite** - lightweight SQL database
- **Pydantic** - request and response validation
- **Uvicorn** - ASGI server
- **Pytest** - automated testing
- **Docker** - optional containerized local deployment

### Why this stack?

This combination is especially suitable for coursework because:

- FastAPI is beginner-friendly and concise
- Swagger documentation is generated automatically
- SQLite requires no separate database server setup
- SQLAlchemy demonstrates ORM-based database design
- Pydantic clearly shows input validation and typed responses
- Docker adds an extra professional feature for portability

## 3. Project Structure

```text
web1/
├── routers/
│   ├── __init__.py
│   └── items.py
├── .dockerignore
├── .env.example
├── Dockerfile
├── database.py
├── main.py
├── README.md
├── requirements.txt
├── schemas.py
├── seed_data.py
└── test_main.py
```

## 4. File Responsibilities

### `main.py`
Creates the FastAPI application, enables middleware, registers custom exception handlers, initializes the database tables, and mounts the API router.

### `database.py`
Contains the SQLite connection, SQLAlchemy session factory, ORM base class, and the `Task` database model with timestamps.

### `schemas.py`
Defines the Pydantic schemas used for validating request bodies and formatting JSON responses, including paginated responses and standardized error payloads.

### `routers/items.py`
Implements all task-related API endpoints, including CRUD, pagination, filtering, searching, and partial updates.

### `seed_data.py`
Inserts sample tasks into the database for demonstrations and screenshots.

### `test_main.py`
Provides automated tests for the API using a fully isolated temporary database.

### `Dockerfile`
Allows the application to run inside a Docker container.

## 5. Features Implemented

This version is stronger than a minimal CRUD submission and looks more like a formal coursework project.

### Core features

- Create a task
- Read all tasks
- Read one task by ID
- Replace a task using `PUT`
- Delete a task

### Additional professional features

- Pagination support using `page` and `limit`
- Search tasks by title using `search`
- Filter tasks by completion status using `completed`
- Partial updates using `PATCH`
- Automatic creation and update timestamps
- Standardized JSON error responses
- Seed data script for demonstrations
- Docker support for containerized execution
- Basic automated endpoint tests
- Structured list responses with pagination metadata

## 6. Installation and Setup

### Step 1: Create a virtual environment

#### Windows PowerShell

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

## 7. Environment Variables

A sample environment configuration is provided in `.env.example`.

To create a local `.env` file on Windows:

```bash
copy .env.example .env
```

Example:

```env
DATABASE_URL=sqlite:///./tasks.db
APP_NAME=Task Management API
APP_VERSION=1.0.0
```

## 8. Database Initialization

No separate migration tool is required for this beginner-friendly submission.
The application creates the database file and `tasks` table automatically when the server starts.

After the first run, a local SQLite database file named `tasks.db` will be created in the project folder.

## 9. Seed Sample Data

To insert sample tasks for testing or coursework demonstration:

```bash
python seed_data.py
```

This script avoids duplicating data if tasks already exist.

## 10. Running the Application

Start the development server with:

```bash
uvicorn main:app --reload
```

The application will be available at:

- `http://127.0.0.1:8000`

## 11. API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

These pages are very useful for coursework screenshots and demonstrations.

## 12. API Endpoints

### 1. Root endpoint

- **Method:** `GET`
- **URL:** `/`
- **Purpose:** Confirm the API is running
- **Status code:** `200 OK`

Example:

```bash
curl -X GET "http://127.0.0.1:8000/"
```

### 2. Get all tasks with pagination and filters

- **Method:** `GET`
- **URL:** `/api/tasks?page=1&limit=10`
- **Optional query parameters:**
  - `search` - search by title keyword
  - `completed` - filter by `true` or `false`
- **Status code:** `200 OK`

Examples:

```bash
curl -X GET "http://127.0.0.1:8000/api/tasks?page=1&limit=10"
```

```bash
curl -X GET "http://127.0.0.1:8000/api/tasks?page=1&limit=10&search=coursework"
```

```bash
curl -X GET "http://127.0.0.1:8000/api/tasks?completed=true"
```

### 3. Get one task by ID

- **Method:** `GET`
- **URL:** `/api/tasks/{task_id}`
- **Success code:** `200 OK`
- **Error code:** `404 Not Found`

Example:

```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/1"
```

### 4. Create a task

- **Method:** `POST`
- **URL:** `/api/tasks`
- **Success code:** `201 Created`
- **Validation error:** `422 Unprocessable Entity`

Example:

```bash
curl -X POST "http://127.0.0.1:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Finish coursework\",\"description\":\"Build backend API and write report\",\"completed\":false,\"due_date\":\"2026-04-30\"}"
```

### 5. Replace a task using PUT

- **Method:** `PUT`
- **URL:** `/api/tasks/{task_id}`
- **Success code:** `200 OK`
- **Error code:** `404 Not Found`

Example:

```bash
curl -X PUT "http://127.0.0.1:8000/api/tasks/1" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Finish coursework and presentation\",\"description\":\"Update API and prepare demo slides\",\"completed\":true,\"due_date\":\"2026-05-02\"}"
```

### 6. Partially update a task using PATCH

- **Method:** `PATCH`
- **URL:** `/api/tasks/{task_id}`
- **Success code:** `200 OK`
- **Error code:** `404 Not Found`

Example:

```bash
curl -X PATCH "http://127.0.0.1:8000/api/tasks/1" \
  -H "Content-Type: application/json" \
  -d "{\"completed\":true}"
```

### 7. Delete a task

- **Method:** `DELETE`
- **URL:** `/api/tasks/{task_id}`
- **Success code:** `200 OK`
- **Error code:** `404 Not Found`

Example:

```bash
curl -X DELETE "http://127.0.0.1:8000/api/tasks/1"
```

## 13. Example JSON Responses

### Example create/get response

```json
{
  "id": 1,
  "title": "Finish coursework",
  "description": "Build backend API and write report",
  "completed": false,
  "due_date": "2026-04-30",
  "created_at": "2026-04-05T10:30:00Z",
  "updated_at": "2026-04-05T10:30:00Z"
}
```

### Example list response

```json
{
  "page": 1,
  "limit": 10,
  "total": 3,
  "items": [
    {
      "id": 1,
      "title": "Finish coursework",
      "description": "Build backend API and write report",
      "completed": false,
      "due_date": "2026-04-30",
      "created_at": "2026-04-05T10:30:00Z",
      "updated_at": "2026-04-05T10:30:00Z"
    }
  ]
}
```

### Example delete response

```json
{
  "message": "Task 1 deleted successfully"
}
```

### Example standardized error response

```json
{
  "error": "HTTP error",
  "detail": "Task not found",
  "status_code": 404,
  "path": "/api/tasks/999999"
}
```

## 14. HTTP Status Codes Used

- `200 OK` - successful GET, PUT, PATCH, and DELETE requests
- `201 Created` - successful POST request
- `404 Not Found` - requested resource does not exist
- `422 Unprocessable Entity` - invalid request body or query data
- `500 Internal Server Error` - unexpected server failure

## 15. Automated Testing

This project includes `pytest`-based tests.

To run the tests:

```bash
pytest
```

The tests cover:

- Root endpoint
- Create task
- List tasks
- Get task by ID
- Full update with `PUT`
- Partial update with `PATCH`
- Search and filtering
- Delete endpoint
- `404` error handling
- `422` validation handling
- Timestamp presence in API responses

### Test isolation

The test suite uses a separate temporary SQLite database so that testing does not modify the main development database.

## 16. Docker Usage

You can also run the API with Docker.

### Build the Docker image

```bash
docker build -t task-management-api .
```

### Run the Docker container

```bash
docker run -p 8000:8000 task-management-api
```

Then open:

- `http://127.0.0.1:8000/docs`

## 17. Suggested Demonstration for Coursework Submission

If you need to present or record this project, a good demonstration sequence is:

1. Show the project folder structure
2. Run the server with `uvicorn main:app --reload`
3. Insert demo records with `python seed_data.py`
4. Open Swagger UI at `/docs`
5. Create a new task
6. Show the task appearing in the list endpoint
7. Search/filter the tasks
8. Update a task using `PUT`
9. Update a single field using `PATCH`
10. Delete the task
11. Show custom JSON error handling with a non-existent ID
12. Run automated tests with `pytest`

## 18. Report-Writing Talking Points

You can use the following ideas in your coursework report:

### System design
- The API follows a resource-based REST style
- FastAPI handles routing and validation
- SQLAlchemy maps Python classes to relational database tables
- SQLite provides lightweight persistent storage
- Timestamps improve auditability of records

### Validation and errors
- Pydantic ensures incoming request bodies follow the required structure
- Invalid data automatically returns a `422` response
- Custom exception handlers provide a consistent JSON error format

### Data persistence
- Data is stored in a `tasks` table inside a SQLite database file
- SQLAlchemy sessions handle creation, reading, updating, and deletion of records

### Extensibility
- The project can be expanded with authentication, advanced filtering, or PostgreSQL deployment
- Docker support improves portability across environments

## 19. Deployment Suggestions

### Deploy to Render

1. Push the project to GitHub
2. Create a new Web Service on Render
3. Set the start command to:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

4. Add any required environment variables
5. Deploy and test the live URL

### Deploy to PythonAnywhere

1. Upload the project files
2. Create a virtual environment
3. Install dependencies using `pip install -r requirements.txt`
4. Configure an ASGI web application

## 20. Exporting OpenAPI / Swagger Documentation to PDF

Since FastAPI generates OpenAPI automatically, documentation export is straightforward.

### Option 1: Browser print to PDF
1. Start the API
2. Visit `http://127.0.0.1:8000/docs`
3. Use the browser's print feature
4. Save as PDF

### Option 2: Export OpenAPI JSON
1. Visit `http://127.0.0.1:8000/openapi.json`
2. Save the JSON file
3. Import it into Swagger tooling or documentation generators
4. Convert the generated docs into PDF format

## 21. Possible Future Enhancements

- Add user authentication and authorization
- Add task sorting options
- Add database migrations with Alembic
- Add frontend integration
- Add Docker Compose support
- Deploy with PostgreSQL instead of SQLite

## 22. Conclusion

This project provides a clean, well-documented, and coursework-appropriate example of a RESTful Web API. It demonstrates database-backed CRUD operations, request validation, HTTP status code usage, automated API documentation, consistent error handling, timestamps, sample data seeding, Docker support, and isolated automated testing in a way that is suitable for both beginner learning and formal submission.
