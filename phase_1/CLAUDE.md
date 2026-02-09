# Phase 1 Todo Manager - In-Memory CLI Application

## Project Overview

This is a console-based todo manager application built for Hackathon Phase 1. It operates entirely in-memory with volatile data storage, meaning all data resets when the application restarts. This implementation follows the Spec-Driven Development (SDD) methodology and serves as a foundation for future phases.

## Features

- Add new todo items with titles and descriptions
- List all todo items with their status
- Update existing todo items (title and/or description)
- Mark todo items as completed
- Delete todo items
- All data is stored in-memory (volatile, no file persistence)

## Commands

### Add a Todo
```bash
python main.py add "Task Title" "Optional Description"
```

### List Todos
```bash
python main.py list
```

### Update a Todo
```bash
python main.py update <id> "New Title" "Optional New Description"
```

### Complete a Todo
```bash
python main.py complete <id>
```

### Delete a Todo
```bash
python main.py delete <id>
```

### Help
```bash
python main.py --help
```

## Technical Details

- Language: Python
- Storage: In-memory Python list/dictionary (volatile)
- Data Model: Each todo has an ID, title, description, status, and creation timestamp
- Architecture: CLI interface with separate business logic module
- Data resets on application restart (no permanent storage)

## Limitations

- Data is not persisted to disk
- All todos are lost when the application closes
- Designed as a proof-of-concept for Phase 1