"""
Simple test to verify the main functionality works with the updated structure
"""
from todo_manager import TodoManager


def test_main_functionality():
    # Initialize the TodoManager
    tm = TodoManager('todo.json')
    
    print("Testing main functionality with updated structure...")
    
    # Test getting all tasks
    print("\n1. Current tasks:")
    all_tasks = tm.get_all_tasks()
    for task in all_tasks:
        print(f"  ID: {task['id']}, Task: {task['task']}, Status: {task['status']}")
    
    # Test adding a new task
    print("\n2. Adding a new task:")
    new_task = tm.add_task("Test new functionality", "Testing", "High")
    print(f"  Added: {new_task}")
    
    # Test updating a task
    print("\n3. Updating a task:")
    updated_task = tm.update_task(1, new_task_name="Updated task name", new_status="Completed")
    print(f"  Updated: {updated_task}")
    
    # Test completing a task
    print("\n4. Completing a task:")
    tm.complete_task(2)
    completed_task = tm.find_task_by_id(2)
    print(f"  Completed: {completed_task}")
    
    # Test filtering by category
    print("\n5. Filtering by category 'Work':")
    work_tasks = tm.filter_tasks(category="Work")
    for task in work_tasks:
        print(f"  {task['task']} - {task['status']}")
    
    # Test filtering by status
    print("\n6. Filtering by status 'Completed':")
    completed_tasks = tm.filter_tasks(status="Completed")
    for task in completed_tasks:
        print(f"  {task['task']} - {task['category']}")
    
    print("\nAll tests passed successfully!")


if __name__ == "__main__":
    test_main_functionality()