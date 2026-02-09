# Full-Stack Web Application - Monorepo

## Overview
This is a full-stack web application built with a Next.js frontend and FastAPI backend, using Neon Serverless PostgreSQL as the database. The application implements secure task management with JWT-based authentication.

## Architecture
- Frontend: Next.js 15+ (App Router), Tailwind CSS
- Backend: FastAPI (Python) with SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth (JWT plugin enabled)

## Monorepo Structure
```
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   └── ...
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── auth.py
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   ├── database.py
│   ├── config.py
│   └── requirements.txt
├── specs/
│   ├── database/
│   │   └── schema.md
│   └── api/
│       └── endpoints.md
├── README.md
└── CLAUDE.md (this file)
```

## Tech Stack
- **Frontend**: Next.js 15+, React, Tailwind CSS, Better Auth client
- **Backend**: FastAPI, SQLModel, Pydantic, Uvicorn
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT
- **Deployment**: Vercel (frontend), Railway/Render (backend)

## Development
- Frontend runs on port 3000
- Backend runs on port 8000
- Database connection via Neon PostgreSQL
- Authentication handled by Better Auth

## Environment Variables
- `DATABASE_URL`: Connection string for Neon PostgreSQL
- `BETTER_AUTH_SECRET`: Secret key for JWT token verification
- `BETTER_AUTH_URL`: URL of the Better Auth service