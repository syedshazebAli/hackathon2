import json
import os
from rich.console import Console
from rich.table import Table


class TodoManager:
    """Manages tasks with persistence to JSON file."""
    
    def __init__(self, file_path='tasks.json'):
        self.file_path = file_path
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from the JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    
                    # Handle both formats: array of tasks or object with tasks property
                    if isinstance(data, list):
                        # Format: [{"id": 1, "task": "...", ...}]
                        return data
                    elif isinstance(data, dict) and 'tasks' in data:
                        # Format: {"tasks": [{"id": 1, "task": "...", ...}]}
                        return data['tasks']
                    else:
                        # Unexpected format, return empty list
                        return []
                        
                except json.JSONDecodeError:
                    # If file is corrupted, return empty list
                    return []
        else:
            # Create file with empty list if it doesn't exist
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []
    
    def save_tasks(self):
        """Save tasks to the JSON file."""
        # Determine the format based on the original file structure
        # If the file exists and has the object format, maintain it
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                try:
                    original_data = json.load(file)
                    if isinstance(original_data, dict) and 'tasks' in original_data:
                        # Save in object format
                        data_to_save = {"tasks": self.tasks}
                    else:
                        # Save in array format
                        data_to_save = self.tasks
                except json.JSONDecodeError:
                    # If original file is corrupted, save in array format
                    data_to_save = self.tasks
        else:
            # New file, save in array format
            data_to_save = self.tasks
            
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4)
    
    def get_next_id(self):
        """Get the next available ID for a new task."""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1
    
    def add_task(self, task_name, category="General", priority="Medium"):
        """Add a new task to the list."""
        if not task_name.strip():
            raise ValueError("Task name cannot be empty!")
        
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be 'High', 'Medium', or 'Low'")
        
        new_task = {
            'id': self.get_next_id(),
            'task': task_name.strip(),
            'category': category.strip(),
            'priority': priority,
            'status': 'Pending'
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task
    
    def view_tasks(self):
        """Display all tasks in a table format."""
        if not self.tasks:
            print("No tasks found.")
            return
        
        console = Console(force_terminal=True)
        table = Table(title="Tasks List")
        
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Task", style="magenta")
        table.add_column("Category", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Status", style="red")
        
        for task in self.tasks:
            status_color = "green" if task['status'] == 'Completed' else "red"
            table.add_row(
                str(task['id']),
                task['task'],
                task['category'],
                task['priority'],
                f"[{status_color}]{task['status']}[/{status_color}]"
            )
        
        console.print(table)
    
    def update_task(self, task_id, new_task_name=None, new_status=None):
        """Update an existing task."""
        task = self.find_task_by_id(task_id)
        if not task:
            raise ValueError(f"No task found with ID {task_id}")
        
        if new_task_name is not None:
            task['task'] = new_task_name.strip()
        
        if new_status is not None:
            if new_status not in ['Completed', 'Pending']:
                raise ValueError("Status must be 'Completed' or 'Pending'")
            task['status'] = new_status
        
        self.save_tasks()
        return task
    
    def complete_task(self, task_id):
        """Mark a task as completed."""
        return self.update_task(task_id, new_status='Completed')
    
    def delete_task(self, task_id):
        """Delete a task by ID."""
        task = self.find_task_by_id(task_id)
        if not task:
            raise ValueError(f"No task found with ID {task_id}")
        
        self.tasks.remove(task)
        self.save_tasks()
        return task
    
    def find_task_by_id(self, task_id):
        """Find a task by its ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def filter_tasks(self, **filters):
        """Filter tasks by given criteria."""
        filtered_tasks = self.tasks
        
        for key, value in filters.items():
            if key in ['category', 'status', 'priority']:
                filtered_tasks = [
                    task for task in filtered_tasks 
                    if task.get(key, '').lower() == value.lower()
                ]
        
        return filtered_tasks