import json
import os
from rich.console import Console
from rich.table import Table
from src.todo_manager import TodoManager


def add_task_ui(todo_manager):
    """UI wrapper for adding a task."""
    task_name = input("Enter task name: ").strip()
    if not task_name:
        print("Task name cannot be empty!")
        return
    
    category = input("Enter category: ").strip()
    if not category:
        category = "General"  # Default category
    
    while True:
        priority_input = input("Enter priority (H/M/L): ").strip().upper()
        if priority_input == 'H':
            priority = "High"
            break
        elif priority_input == 'M':
            priority = "Medium"
            break
        elif priority_input == 'L':
            priority = "Low"
            break
        else:
            print("Invalid input. Please enter H for High, M for Medium, or L for Low.")
    
    try:
        new_task = todo_manager.add_task(task_name, category, priority)
        print(f"Task '{new_task['task']}' added successfully!")
    except ValueError as e:
        print(f"Error adding task: {e}")


def view_tasks_ui(todo_manager):
    """UI wrapper for viewing tasks."""
    todo_manager.view_tasks()


def update_task_ui(todo_manager):
    """UI wrapper for updating a task."""
    if not todo_manager.tasks:
        print("No tasks found.")
        return
    
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    task = todo_manager.find_task_by_id(task_id)
    if not task:
        print(f"No task found with ID {task_id}.")
        return
    
    print(f"Current task: {task['task']}")
    print(f"Current status: {task['status']}")
    
    update_choice = input("What would you like to update? (1) Task name, (2) Status, (3) Both: ").strip()
    
    new_task_name = None
    new_status = None
    
    if update_choice in ['1', '3']:
        new_task_name_input = input("Enter new task name (or press Enter to keep current): ").strip()
        if new_task_name_input:
            new_task_name = new_task_name_input
    
    if update_choice in ['2', '3']:
        while True:
            new_status_input = input("Enter new status (Completed/Pending) or press Enter to keep current: ").strip().capitalize()
            if new_status_input in ['', 'Completed', 'Pending']:
                if new_status_input:
                    new_status = new_status_input
                break
            else:
                print("Invalid status. Please enter 'Completed' or 'Pending'.")
    
    try:
        updated_task = todo_manager.update_task(task_id, new_task_name, new_status)
        print("Task updated successfully!")
    except ValueError as e:
        print(f"Error updating task: {e}")


def complete_task_ui(todo_manager):
    """UI wrapper for completing a task."""
    if not todo_manager.tasks:
        print("No tasks found.")
        return
    
    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    try:
        todo_manager.complete_task(task_id)
        print(f"Task with ID {task_id} marked as completed!")
    except ValueError as e:
        print(f"Error completing task: {e}")


def delete_task_ui(todo_manager):
    """UI wrapper for deleting a task."""
    if not todo_manager.tasks:
        print("No tasks found.")
        return
    
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    try:
        deleted_task = todo_manager.delete_task(task_id)
        print(f"Task '{deleted_task['task']}' with ID {task_id} deleted successfully!")
    except ValueError as e:
        print(f"Error deleting task: {e}")


def filter_tasks_ui(todo_manager):
    """UI wrapper for filtering tasks."""
    if not todo_manager.tasks:
        print("No tasks found.")
        return
    
    filter_choice = input("Filter by (1) Category or (2) Status: ").strip()
    
    if filter_choice == '1':
        category = input("Enter category to filter by: ").strip()
        filtered_tasks = todo_manager.filter_tasks(category=category)
        print(f"\nTasks in category '{category}':")
    elif filter_choice == '2':
        status = input("Enter status to filter by (Completed/Pending): ").strip().capitalize()
        if status not in ['Completed', 'Pending']:
            print("Invalid status. Please enter 'Completed' or 'Pending'.")
            return
        filtered_tasks = todo_manager.filter_tasks(status=status)
        print(f"\nTasks with status '{status}':")
    else:
        print("Invalid choice.")
        return
    
    if not filtered_tasks:
        print("No tasks found matching the filter.")
        return
    
    console = Console(force_terminal=True)
    table = Table(title=f"Filtered Tasks ({'Category' if filter_choice == '1' else 'Status'})")
    
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="red")
    
    for task in filtered_tasks:
        status_color = "green" if task['status'] == 'Completed' else "red"
        table.add_row(
            str(task['id']),
            task['task'],
            task['category'],
            task['priority'],
            f"[{status_color}]{task['status']}[/{status_color}]"
        )
    
    console.print(table)


def main():
    """Main function to run the Todo Manager."""
    todo_manager = TodoManager()
    
    while True:
        print("\n" + "="*50)
        print("TODO MANAGER - FUNCTIONAL MENU")
        print("="*50)
        print("[1] Add Task")
        print("[2] View All Tasks")
        print("[3] Update Task")
        print("[4] Complete Task")
        print("[5] Delete Task")
        print("[6] Search/Filter Tasks")
        print("[7] Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            add_task_ui(todo_manager)
        elif choice == '2':
            view_tasks_ui(todo_manager)
        elif choice == '3':
            update_task_ui(todo_manager)
        elif choice == '4':
            complete_task_ui(todo_manager)
        elif choice == '5':
            delete_task_ui(todo_manager)
        elif choice == '6':
            filter_tasks_ui(todo_manager)
        elif choice == '7':
            print("Thank you for using Todo Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()