# Task Manager API

A production-ready REST API for managing tasks with user authentication, built with FastAPI and PostgreSQL.

## Features

- User registration and authentication with JWT
- Complete CRUD operations for tasks
- Pagination and advanced filtering
- Input validation with Pydantic
- Comprehensive test suite
- OpenAPI documentation

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 12+

### Installation

1. Clone the repository:

git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api

2. Create and activate virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Create `.env` file from `.env.example`:

cp .env.example .env

5. Update `.env` with your PostgreSQL credentials.

6. Run database migrations:

alembic upgrade head

7. Start the server:

uvicorn app.main:app --reload

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Testing

pytest

## Project Structure

task-manager-api/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # API endpoints
│   └── main.py           # FastAPI app
├── tests/                # Test suite
├── requirements.txt      # Python dependencies
└── .env.example          # Environment variables example

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Tasks
- `POST /tasks` - Create task
- `GET /tasks` - List user tasks
- `GET /tasks/{task_id}` - Get task detail
- `PATCH /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task