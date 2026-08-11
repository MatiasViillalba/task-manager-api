# Task Manager API

A REST API for managing personal tasks, built with Python, FastAPI, PostgreSQL, and JWT authentication.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens&logoColor=white)

## ✨ Features

- User registration and login with JWT authentication
- Complete CRUD operations for tasks
- Pagination, sorting, and advanced filtering (status, priority, due date range)
- Input validation with Pydantic
- Ownership-based authorization (users only access their own tasks)
- Global error handling and request logging middleware
- Database migrations with Alembic
- Comprehensive automated test suite (unit and integration tests)
- OpenAPI/Swagger documentation
- Docker support

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Authentication:** JWT (python-jose) + bcrypt (passlib)
- **Migrations:** Alembic
- **Testing:** pytest
- **Containerization:** Docker

## 📁 Project Structure

    task-manager-api/
    ├── app/
    │   ├── models/            
    │   ├── schemas/           
    │   ├── routes/           
    │   ├── main.py           
    │   ├── config.py          
    │   ├── database.py      
    │   ├── security.py        
    │   ├── dependencies.py   
    │   └── exceptions.py      
    ├── alembic/               
    ├── tests/                  
    │   ├── conftest.py         
    │   ├── test_auth.py         
    │   ├── test_tasks.py        
    │   └── test_integration.py 
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── pytest.ini
    ├── .env.example
    └── README.md

## 🚀 Setup (local development)

### Prerequisites

- Python 3.10+
- PostgreSQL 12+

### Installation

1. Clone the repository:

       git clone https://github.com/MatiasViillalba/task-manager-api.git
       cd task-manager-api

2. Create and activate a virtual environment:

       python -m venv venv
       source venv/Scripts/activate  # On Windows (Git Bash)

3. Install dependencies:

       pip install -r requirements.txt

4. Create a `.env` file from `.env.example` and fill in your PostgreSQL credentials:

       cp .env.example .env

5. Run database migrations:

       alembic upgrade head

6. Start the development server:

       uvicorn app.main:app --reload

The API will be available at `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

## 🐳 Setup (Docker)

1. Create a `.env` file with at least a `SECRET_KEY` value.

2. Build and start the containers:

       docker-compose up --build

The API will be available at `http://localhost:8000`

## 🧪 Running Tests

    pytest -v

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Log in and receive a JWT access token |

### Tasks (require authentication)

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List tasks (supports pagination, sorting, filtering) |
| GET | `/tasks/{task_id}` | Get a single task by ID |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Query Parameters for `GET /tasks`

| Parameter | Description | Default |
|-----------|--------------|---------|
| `limit` | Maximum number of results | 10 |
| `offset` | Number of results to skip | 0 |
| `status` | Filter by status (pending, in_progress, completed) | none |
| `priority` | Filter by priority (low, medium, high) | none |
| `due_date_from` | Filter tasks due on or after this date | none |
| `due_date_to` | Filter tasks due on or before this date | none |
| `sort_by` | Field to sort by (created_at, updated_at, status, priority, title) | created_at |
| `sort_order` | Sort direction (asc, desc) | desc |
