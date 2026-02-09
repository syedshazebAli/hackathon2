# Database Schema

## Overview
The database uses Neon Serverless PostgreSQL with tables designed for user authentication and task management. The schema supports secure user isolation and efficient querying.

## Tables

### users
Stores user account information.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### tasks
Stores individual tasks associated with users.

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in-progress', 'completed')),
    priority VARCHAR(50) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    category VARCHAR(100),
    due_date TIMESTAMP WITH TIME ZONE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);
```

## Indexes
For optimal performance, the following indexes are recommended:

```sql
-- Index on user_id for efficient user-specific queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index on status for filtering tasks by status
CREATE INDEX idx_tasks_status ON tasks(status);

-- Index on due_date for sorting and filtering by deadline
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- Composite index for common filtering combinations
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

## Relationships
- One user can have many tasks (one-to-many relationship)
- Tasks are automatically deleted when the associated user is deleted (CASCADE)

## Constraints
- Email uniqueness in users table
- Status values restricted to predefined options
- Priority values restricted to predefined options
- Foreign key constraint ensures referential integrity

## Notes
- UUIDs are used for primary keys to ensure global uniqueness
- Timestamps are stored with timezone information
- The `completed_at` field is nullable and only populated when status is 'completed'