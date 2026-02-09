import json
import os
from datetime import datetime


class TodoManager:
    def __init__(self, file_path='todo.json'):
        self.file_path = file_path
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            # Create file with default structure
            default_data = {"tasks": []}
            self.save_data(default_data)
            return default_data
    
    def save_data(self, data=None):
        if data is None:
            data = self.data
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def get_next_id(self):
        if not self.data['tasks']:
            return 1
        return max(task['id'] for task in self.data['tasks']) + 1
    
    def add_task(self, task_name, category="General", priority="Medium"):
        if not task_name.strip():
            raise ValueError("Task name cannot be empty!")
        
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be 'High', 'Medium', or 'Low'")
        
        new_task = {
            'id': self.get_next_id(),
            'task': task_name.strip(),
            'category': category.strip(),
            'priority': priority,
            'status': 'Pending',
            'created_at': datetime.now().isoformat()
        }
        
        self.data['tasks'].append(new_task)
        self.save_data()
        return new_task
    
    def get_all_tasks(self):
        return self.data['tasks']
    
    def update_task(self, task_id, new_task_name=None, new_status=None):
        task = self.find_task_by_id(task_id)
        if not task:
            raise ValueError(f"No task found with ID {task_id}")
        
        if new_task_name is not None:
            task['task'] = new_task_name.strip()
        
        if new_status is not None:
            if new_status not in ['Completed', 'Pending']:
                raise ValueError("Status must be 'Completed' or 'Pending'")
            task['status'] = new_status
        
        # Update the timestamp when modifying the task
        task['updated_at'] = datetime.now().isoformat()
        
        self.save_data()
        return task
    
    def complete_task(self, task_id):
        return self.update_task(task_id, new_status='Completed')
    
    def delete_task(self, task_id):
        task = self.find_task_by_id(task_id)
        if not task:
            raise ValueError(f"No task found with ID {task_id}")
        
        self.data['tasks'].remove(task)
        self.save_data()
        return task
    
    def find_task_by_id(self, task_id):
        for task in self.data['tasks']:
            if task['id'] == task_id:
                return task
        return None
    
    def filter_tasks(self, **filters):
        filtered_tasks = self.data['tasks']
        
        for key, value in filters.items():
            if key in ['category', 'status', 'priority']:
                filtered_tasks = [
                    task for task in filtered_tasks 
                    if task.get(key, '').lower() == value.lower()
                ]
        
        return filtered_tasks