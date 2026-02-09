# Todo AI Chatbot - Project Specifications

## Overview
A stateless AI chatbot system that allows users to manage their tasks through natural language conversations. The system uses OpenAI's Agent SDK with MCP tools to provide intelligent task management capabilities.

## Architecture
- Backend: Python FastAPI
- Database: Neon PostgreSQL
- ORM: SQLModel
- AI Logic: OpenAI Agents SDK & Official MCP SDK
- Frontend: Basic ChatKit UI

## Database Schema
### Task Model
- id: UUID (Primary Key)
- title: String (Required)
- description: String (Optional)
- completed: Boolean (Default: False)
- created_at: DateTime (Default: Current timestamp)
- updated_at: DateTime (Default: Current timestamp)
- user_id: UUID (Foreign Key to User)

### Conversation Model
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User)
- title: String (Generated from first message)
- created_at: DateTime (Default: Current timestamp)
- updated_at: DateTime (Default: Current timestamp)

### Message Model
- id: UUID (Primary Key)
- conversation_id: UUID (Foreign Key to Conversation)
- role: String (user/assistant/system)
- content: String (Message content)
- timestamp: DateTime (Default: Current timestamp)

## MCP Tools
### add_task(title: str, description: str = None) -> dict
- Creates a new task for the user
- Returns success message with task details

### list_tasks(completed: bool = None) -> list
- Lists all tasks for the user
- Optionally filter by completion status
- Returns list of task objects

### complete_task(task_id: str) -> dict
- Marks a task as completed
- Returns success message

### delete_task(task_id: str) -> dict
- Deletes a task
- Returns success message

### update_task(task_id: str, title: str = None, description: str = None, completed: bool = None) -> dict
- Updates task properties
- Returns updated task details

## API Endpoints
### POST /api/{user_id}/chat
- Accepts user message in request body
- Fetches conversation history from database
- Stores user message in database
- Runs OpenAI Agent with MCP tools
- Stores AI response in database
- Returns AI response

## Conversation Flow
1. Receive user message
2. Fetch conversation history from DB
3. Store user message in DB
4. Run OpenAI Agent with MCP tools
5. Store AI response in DB
6. Return AI response to user

## Environment Variables
- DATABASE_URL: PostgreSQL connection string
- OPENAI_API_KEY: OpenAI API key

## Error Handling
- Proper error responses with HTTP status codes
- Validation of input data
- Database transaction handling

## Security
- Input validation
- SQL injection prevention via ORM
- Secure API key storage