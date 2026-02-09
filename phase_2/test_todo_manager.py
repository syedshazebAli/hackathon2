"""
Test script for the Todo Manager functionality
"""
import os
import json
from src.todo_manager import TodoManager


def test_todo_manager():
    # Create a temporary tasks file for testing
    test_file = 'test_tasks.json'
    
    # Initialize TodoManager with test file
    tm = TodoManager(test_file)
    
    print("Testing Todo Manager functionality...")
    
    # Test adding tasks
    print("\n1. Testing add_task:")
    task1 = tm.add_task("Test task 1", "Work", "High")
    print(f"Added task: {task1}")
    
    task2 = tm.add_task("Test task 2", "Personal", "Low")
    print(f"Added task: {task2}")
    
    # Test viewing tasks (this will print to console)
    print("\n2. Testing view_tasks:")
    tm.view_tasks()
    
    # Test updating a task
    print("\n3. Testing update_task:")
    updated_task = tm.update_task(task1['id'], new_task_name="Updated test task", new_status="Completed")
    print(f"Updated task: {updated_task}")
    
    # Test completing a task
    print("\n4. Testing complete_task:")
    tm.complete_task(task2['id'])
    completed_task = tm.find_task_by_id(task2['id'])
    print(f"Completed task: {completed_task}")
    
    # Test filtering tasks
    print("\n5. Testing filter_tasks (by status 'Completed'):")
    completed_tasks = tm.filter_tasks(status="Completed")
    print(f"Completed tasks: {completed_tasks}")
    
    print("\n6. Testing filter_tasks (by category 'Work'):")
    work_tasks = tm.filter_tasks(category="Work")
    print(f"Work tasks: {work_tasks}")
    
    # Test deleting a task
    print("\n7. Testing delete_task:")
    deleted_task = tm.delete_task(task1['id'])
    print(f"Deleted task: {deleted_task}")
    
    # Show remaining tasks
    print("\n8. Remaining tasks after deletion:")
    tm.view_tasks()
    
    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\nCleaned up test file: {test_file}")
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_todo_manager()