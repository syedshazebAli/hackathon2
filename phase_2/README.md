# Full-Stack Task Management Application

This is a full-stack web application built with Next.js frontend and FastAPI backend, using Neon Serverless PostgreSQL as the database. The application implements secure task management with JWT-based authentication.

## Architecture

- **Frontend**: Next.js 15+ (App Router), Tailwind CSS, Better Auth
- **Backend**: FastAPI (Python) with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth (JWT plugin enabled)

## Features

- User authentication with Better Auth (Google and GitHub OAuth)
- Secure task management with user isolation
- Responsive dashboard for task management
- CRUD operations for tasks
- Task filtering by status and priority
- JWT token-based authentication

## Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL (or Neon Serverless PostgreSQL)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/taskdb
BETTER_AUTH_SECRET=your-super-secret-key-here-make-it-long-and-random
BETTER_AUTH_URL=http://localhost:8888
```

4. Run the backend server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables in `.env.local`:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8888
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/tasks` - Retrieve user's tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Mark task as completed

All endpoints require JWT Bearer token authentication.

## Database Schema

The application uses the following tables:

### users
- id (UUID, Primary Key)
- email (VARCHAR, Unique)
- name (VARCHAR)
- avatar_url (TEXT)
- email_verified (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### tasks
- id (UUID, Primary Key)
- title (VARCHAR, Not Null)
- description (TEXT)
- status (VARCHAR, Default: 'pending')
- priority (VARCHAR, Default: 'medium')
- category (VARCHAR)
- due_date (TIMESTAMP)
- user_id (UUID, Foreign Key to users.id)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- completed_at (TIMESTAMP)

## Authentication

Authentication is handled by Better Auth, which provides secure JWT token-based authentication. The frontend sends the JWT token in the Authorization header for all API requests to the backend.

## Development

For development, both the frontend and backend need to be running simultaneously. The frontend proxies API requests to the backend server.

## Deployment

For production deployment:

- Frontend: Deploy to Vercel with proper environment variables
- Backend: Deploy to Railway, Render, or similar platforms
- Database: Use Neon Serverless PostgreSQL or other compatible provider