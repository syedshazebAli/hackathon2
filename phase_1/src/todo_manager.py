from datetime import datetime
from typing import List, Dict, Optional


class TodoManager:
    """Manages todo items with in-memory storage (volatile)."""

    def __init__(self):
        # Initialize empty in-memory storage
        self.todos: List[Dict] = []
        self.next_id: int = 1

    def get_next_id(self) -> int:
        """Gets the next available ID."""
        current_max_id = max([todo.get('id', 0) for todo in self.todos], default=0)
        return current_max_id + 1

    def add_todo(self, task: str, description: str = "", priority: str = "medium", tags: Optional[List[str]] = None) -> Dict:
        """Adds a new todo item."""
        if not task.strip():
            raise ValueError("Task title cannot be empty")
        
        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be 'high', 'medium', or 'low'")
        
        if tags is None:
            tags = []

        new_id = self.get_next_id()

        new_todo = {
            "id": new_id,
            "task": task.strip(),
            "description": description.strip(),
            "status": "pending",
            "priority": priority,
            "tags": tags,
            "created_at": datetime.now().isoformat()
        }

        self.todos.append(new_todo)

        return new_todo

    def list_todos(self) -> List[Dict]:
        """Returns all todos."""
        return self.todos.copy()  # Return a copy to prevent external modification

    def complete_todo(self, todo_id: int) -> bool:
        """Marks a todo as completed."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                if todo['status'] == 'completed':
                    raise ValueError(f"Todo with ID {todo_id} is already completed")

                todo['status'] = 'completed'
                return True

        raise ValueError(f"Todo with ID {todo_id} not found")

    def delete_todo(self, todo_id: int) -> bool:
        """Deletes a specified todo."""
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                del self.todos[i]
                return True

        raise ValueError(f"Todo with ID {todo_id} not found")

    def update_todo(self, todo_id: int, new_task: Optional[str] = None, new_description: Optional[str] = None) -> bool:
        """Updates an existing todo's task title and/or description."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                if new_task is not None:
                    if not new_task.strip():
                        raise ValueError("Task title cannot be empty")
                    todo['task'] = new_task.strip()

                if new_description is not None:
                    todo['description'] = new_description.strip()

                return True

        raise ValueError(f"Todo with ID {todo_id} not found")

    def set_priority(self, todo_id: int, priority: str) -> bool:
        """Sets priority for a specific todo."""
        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be 'high', 'medium', or 'low'")
            
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['priority'] = priority
                return True

        raise ValueError(f"Todo with ID {todo_id} not found")

    def add_tags(self, todo_id: int, tags: List[str]) -> bool:
        """Adds tags to a specific todo."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                # Add new tags without duplicates
                for tag in tags:
                    if tag not in todo['tags']:
                        todo['tags'].append(tag)
                return True

        raise ValueError(f"Todo with ID {todo_id} not found")

    def get_todo_by_id(self, todo_id: int) -> Dict:
        """Retrieves a specific todo by ID."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo.copy()  # Return a copy to prevent external modification

        raise ValueError(f"Todo with ID {todo_id} not found")

    def search_todos(self, keyword: str) -> List[Dict]:
        """Searches todos by keyword in task or description."""
        keyword_lower = keyword.lower()
        results = []
        
        for todo in self.todos:
            if (keyword_lower in todo['task'].lower() or 
                keyword_lower in todo['description'].lower()):
                results.append(todo.copy())
                
        return results

    def filter_todos(self, filter_type: str, filter_value: str) -> List[Dict]:
        """Filters todos by status, priority, or tag."""
        results = []
        
        if filter_type == "status":
            if filter_value not in ["pending", "completed"]:
                raise ValueError("Status must be 'pending' or 'completed'")
            results = [todo for todo in self.todos if todo['status'] == filter_value]
        elif filter_type == "priority":
            if filter_value not in ["high", "medium", "low"]:
                raise ValueError("Priority must be 'high', 'medium', or 'low'")
            results = [todo for todo in self.todos if todo['priority'] == filter_value]
        elif filter_type == "tag":
            results = [todo for todo in self.todos if filter_value in todo['tags']]
        else:
            raise ValueError("Filter type must be 'status', 'priority', or 'tag'")
            
        return results

    def sort_todos(self, sort_type: str) -> List[Dict]:
        """Sorts todos by priority or ID."""
        if sort_type == "priority":
            # Define priority order: high > medium > low
            priority_order = {"high": 3, "medium": 2, "low": 1}
            sorted_todos = sorted(self.todos, 
                                  key=lambda x: priority_order[x['priority']], 
                                  reverse=True)  # High to low priority
        elif sort_type == "id":
            sorted_todos = sorted(self.todos, 
                                  key=lambda x: x['id'])  # Ascending by ID
        else:
            raise ValueError("Sort type must be 'priority' or 'id'")
            
        return sorted_todos


# The example usage in main() has been removed since this is now a module
# To test functionality, run the CLI from main.py