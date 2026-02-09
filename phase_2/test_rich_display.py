"""
Final test to verify the main functionality with rich table display
"""
from src.todo_manager import TodoManager


def test_rich_display():
    # Initialize the TodoManager with tasks.json
    tm = TodoManager('tasks.json')
    
    print("Testing rich table display...")
    tm.view_tasks()
    
    print("\nTesting filter functionality...")
    print("Tasks with status 'Completed':")
    completed_tasks = tm.filter_tasks(status="Completed")
    for task in completed_tasks:
        print(f"  - {task['task']} (ID: {task['id']})")
    
    print("\nTesting filter by category 'Work':")
    work_tasks = tm.filter_tasks(category="Work")
    for task in work_tasks:
        print(f"  - {task['task']} (Status: {task['status']})")


if __name__ == "__main__":
    test_rich_display()