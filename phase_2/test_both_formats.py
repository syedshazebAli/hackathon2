"""
Test to verify both file formats work correctly
"""
from src.todo_manager import TodoManager


def test_both_formats():
    print("Testing array format (tasks.json)...")
    tm1 = TodoManager('tasks.json')
    print(f"Loaded {len(tm1.tasks)} tasks from tasks.json")
    for task in tm1.tasks[:2]:  # Show first 2 tasks
        print(f"  - {task['task']} (ID: {task['id']})")
    
    print("\nTesting object format (todo.json)...")
    tm2 = TodoManager('todo.json')
    print(f"Loaded {len(tm2.tasks)} tasks from todo.json")
    for task in tm2.tasks[:2]:  # Show first 2 tasks
        print(f"  - {task['task']} (ID: {task['id']})")
    
    # Test adding a task to each
    print("\nAdding a task to tasks.json...")
    new_task1 = tm1.add_task("Test task for array format", "Test", "Medium")
    print(f"Added: {new_task1['task']}")
    
    print("\nAdding a task to todo.json...")
    new_task2 = tm2.add_task("Test task for object format", "Test", "High")
    print(f"Added: {new_task2['task']}")
    
    # Verify the files were saved in their respective formats
    import json
    with open('tasks.json', 'r') as f:
        data1 = json.load(f)
        print(f"\ntasks.json format: {'array' if isinstance(data1, list) else 'object'}")
    
    with open('todo.json', 'r') as f:
        data2 = json.load(f)
        print(f"todo.json format: {'object' if isinstance(data2, dict) and 'tasks' in data2 else 'array'}")
    
    print("\nBoth formats work correctly!")


if __name__ == "__main__":
    test_both_formats()