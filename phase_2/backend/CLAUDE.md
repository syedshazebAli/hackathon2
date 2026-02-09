# Backend - FastAPI Application

## Overview
The backend is built with FastAPI, using SQLModel as the ORM for Neon Serverless PostgreSQL. It provides a secure REST API for task management with JWT-based authentication.

## Tech Stack
- FastAPI
- SQLModel
- Pydantic
- Neon Serverless PostgreSQL
- Better Auth JWT integration
- Uvicorn ASGI server

## Directory Structure
```
backend/
├── main.py
├── models.py
├── auth.py
├── database.py
├── config.py
├── api/
│   ├── deps.py
│   └── routes/
│       ├── auth.py
│       └── tasks.py
├── schemas/
│   ├── user.py
│   └── task.py
├── middleware/
│   └── auth_middleware.py
├── utils/
│   └── security.py
└── requirements.txt
```

## Key Features
- Secure REST API endpoints (GET, POST, PUT, DELETE, PATCH)
- JWT token verification using Better Auth secret
- User-specific data filtering (tasks filtered by user_id)
- SQLModel ORM for database operations
- Pydantic models for request/response validation
- Custom authentication middleware

## Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT verification
- `BETTER_AUTH_URL`: Better Auth service URL

## Dependencies
- fastapi
- uvicorn
- sqlmodel
- pydantic
- psycopg2-binary
- python-jose[cryptography]
- passlib[bcrypt]

## API Endpoints
- `GET /api/tasks` - Retrieve user's tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Mark task as completed

## Authentication
- All endpoints require JWT Bearer token
- Token verified using Better Auth shared secret
- Requests validated for user ownership of resources