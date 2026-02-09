# Cloud Native Todo App - Phase 1

This is a command-line todo application that follows Spec-Driven Development methodology. The application implements a comprehensive set of features for managing tasks with priorities, tags, search, filtering, and sorting capabilities.

## Features

### Basic Essentials
- **Add**: Add new todo items with title, description, priority, and tags
- **Delete**: Remove todo items by ID
- **Update**: Update title and description of existing tasks
- **View**: View detailed information about a specific task
- **Mark as Complete**: Mark tasks as completed

### Intermediate Organization
- **Priorities**: Assign priority levels (High/Medium/Low) to tasks
- **Tags**: Add tags (Work/Home/Personal or custom) to tasks
- **Search**: Search tasks by keyword in title or description
- **Filter**: Filter tasks by status, priority, or tag
- **Sort**: Sort tasks by priority or ID

### Technical Implementation
- **In-Memory Storage**: All data is stored in memory (volatile)
- **CLI Interface**: Built with Typer for intuitive command-line usage
- **Rich Output**: Formatted tables and colored output using Rich

## Usage

### Adding Tasks
```bash
# Basic task
todo-cli add "My task"

# Task with description
todo-cli add "My task" "Detailed description"

# Task with priority and tags
todo-cli add "Urgent task" -p high -t work -t urgent
```

### Managing Tasks
```bash
# List all tasks
todo-cli list

# Update a task
todo-cli update 1 "New title" "New description"

# Complete a task
todo-cli complete 1

# Delete a task
todo-cli delete 1

# View detailed info about a task
todo-cli view 1
```

### Organization Features
```bash
# Set priority
todo-cli priority 1 high

# Add tags
todo-cli tag 1 personal important

# Search tasks
todo-cli search "keyword"

# Filter tasks
todo-cli filter status pending
todo-cli filter priority high
todo-cli filter tag work

# Sort tasks
todo-cli sort priority
todo-cli sort id
```

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python -m src.main [command]`

## Architecture

The application consists of:
- `todo_manager.py`: Core business logic and data management
- `main.py`: CLI interface and command routing

## Data Model

Each todo item contains:
```python
{
    "id": int,
    "task": str,
    "description": str,
    "status": str,  # "pending" or "completed"
    "priority": str,  # "high", "medium", or "low"
    "tags": list,  # List of tags
    "created_at": str  # ISO format timestamp
}
```

## Commands Summary

- `add`: Add a new todo item
- `list`: List all todo items
- `update`: Update an existing todo item
- `complete`: Mark a todo as completed
- `delete`: Delete a todo item
- `priority`: Set priority for a todo
- `tag`: Add tags to a todo
- `view`: View detailed info about a todo
- `search`: Search todos by keyword
- `filter`: Filter todos by criteria
- `sort`: Sort todos by priority or ID