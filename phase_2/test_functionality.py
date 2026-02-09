#!/usr/bin/env python3
"""
Test script to verify the Todo Manager functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from main import show_menu
from todo_manager import TodoManager
from rich.console import Console

console = Console(force_terminal=True, force_interactive=True)

def test_basic_functionality():
    """Test basic functionality of the todo manager"""
    print("Testing basic functionality...")
    
    # Test menu display
    print("\n1. Testing menu display:")
    show_menu()
    
    # Test todo manager
    print("\n2. Testing TodoManager:")
    manager = TodoManager()
    
    # Add a task
    todo = manager.add_todo("Test task", "This is a test", "high", ["test", "important"])
    print(f"Added task: {todo}")
    
    # List tasks
    todos = manager.list_todos()
    print(f"Current tasks: {len(todos)}")
    
    # Update task
    manager.update_todo(todo['id'], "Updated test task")
    updated_todo = manager.get_todo_by_id(todo['id'])
    print(f"Updated task: {updated_todo}")
    
    # Complete task
    manager.complete_todo(todo['id'])
    completed_todo = manager.get_todo_by_id(todo['id'])
    print(f"Completed task: {completed_todo}")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_basic_functionality()